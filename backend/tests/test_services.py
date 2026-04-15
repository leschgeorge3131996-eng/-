from __future__ import annotations

import shutil
from pathlib import Path
from uuid import uuid4

import pytest

from backend.app.core.exceptions import ParseError

from backend.app.core.config import Settings
from backend.app.schemas.document import ChunkedDocument, ParsedDocument, ParsedPage, ParsedChunk
from backend.app.schemas.log import CallLogEntry
from backend.app.schemas.task import ResponseDetailLevel
from backend.app.services.chunk_service import ChunkService
from backend.app.services.file_service import FileService
from backend.app.services.log_service import LogService
from backend.app.services.model_client import ModelClient
from backend.app.services.retrieval_service import RetrievalService
from backend.app.services.task_service import TaskService
from backend.app.services.document_parser import DocumentParser


def make_workspace() -> Path:
    root = Path.cwd() / ".test_tmp" / uuid4().hex
    root.mkdir(parents=True, exist_ok=True)
    return root


def cleanup_workspace(path: Path) -> None:
    shutil.rmtree(path, ignore_errors=True)


def build_settings(
    tmp_root: Path,
    *,
    model_lite: str = "",
    model_pro: str = "",
    route_upgrade_chars: int = 12000,
) -> Settings:
    data_dir = tmp_root / "data"
    uploads_dir = data_dir / "uploads"
    parsed_dir = data_dir / "parsed"
    logs_dir = data_dir / "logs"
    cache_dir = data_dir / "cache"
    settings = Settings(
        project_root=tmp_root,
        app_name="test-app",
        app_env="test",
        api_prefix="/api",
        cors_origins=["http://localhost:5173"],
        log_level="INFO",
        max_upload_mb=5,
        max_document_chars=10000,
        request_timeout_seconds=30,
        data_dir=data_dir,
        uploads_dir=uploads_dir,
        parsed_dir=parsed_dir,
        logs_dir=logs_dir,
        cache_dir=cache_dir,
        model_provider="mock",
        use_mock_model=True,
        wuqiong_base_url="",
        wuqiong_api_key="",
        model_lite=model_lite,
        model_pro=model_pro,
        model_qa="mock-qa",
        model_summary="mock-summary",
        model_outline="mock-outline",
        route_upgrade_chars=route_upgrade_chars,
    )
    settings.ensure_directories()
    return settings


def test_save_upload_and_load_text() -> None:
    workspace = make_workspace()
    try:
        settings = build_settings(workspace)
        service = FileService(settings=settings)

        result = service.save_upload("demo.txt", "第一段\n第二段".encode("utf-8"))
        text = service.get_document_text(result.file_id)
        structure = service.get_document_structure(result.file_id)
        chunks = service.get_document_chunks(result.file_id)

        assert result.parse_status == "parsed"
        assert result.text_chars > 0
        assert result.page_count == 1
        assert result.chunk_count >= 1
        assert result.document_fingerprint
        assert structure.page_count == 1
        assert structure.pages[0].text == text
        assert chunks.chunk_count >= 1
        assert "第一段" in text
    finally:
        cleanup_workspace(workspace)


def test_task_service_writes_log() -> None:
    workspace = make_workspace()
    try:
        settings = build_settings(workspace)
        file_service = FileService(settings=settings)
        log_service = LogService(settings=settings)
        model_client = ModelClient(settings=settings)
        task_service = TaskService(
            file_service=file_service,
            model_client=model_client,
            log_service=log_service,
        )

        upload = file_service.save_upload(
            "paper.md",
            "# 标题\n\n这是一个测试文档。\n\n包含研究背景与方法。".encode("utf-8"),
        )
        result = task_service.run_task(
            task_type="summary",
            endpoint="/api/summary",
            file_id=upload.file_id,
            user_input="请突出创新点",
            response_detail_level="detailed",
        )
        logs = log_service.list_logs(limit=10)

        assert result.task_type == "summary"
        assert result.response_detail_level == "detailed"
        assert result.request_id
        assert logs
        assert logs[0]["success"] is True
        assert logs[0]["task_type"] == "summary"
        assert logs[0]["response_detail_level"] == "detailed"
    finally:
        cleanup_workspace(workspace)


class BrokenPdfParser(DocumentParser):
    def extract_text(self, file_path: Path) -> str:
        raise RuntimeError("broken parser")


class FailingLogService(LogService):
    def write_log(self, entry: CallLogEntry) -> None:
        raise OSError("disk full")


class CountingModelClient(ModelClient):
    def __init__(self, settings: Settings) -> None:
        super().__init__(settings=settings)
        self.call_count = 0

    def call_model(
        self,
        task_type: str,
        document_text: str,
        user_input: str | None = None,
        model_name_override: str | None = None,
        response_detail_level: ResponseDetailLevel = "balanced",
    ):
        self.call_count += 1
        return super().call_model(
            task_type,
            document_text,
            user_input,
            model_name_override=model_name_override,
            response_detail_level=response_detail_level,
        )


class RecordingModelClient(ModelClient):
    def __init__(self, settings: Settings) -> None:
        super().__init__(settings=settings)
        self.last_document_text = ""
        self.last_task_type = ""
        self.last_response_detail_level: ResponseDetailLevel = "balanced"

    def call_model(
        self,
        task_type: str,
        document_text: str,
        user_input: str | None = None,
        model_name_override: str | None = None,
        response_detail_level: ResponseDetailLevel = "balanced",
    ):
        self.last_task_type = task_type
        self.last_document_text = document_text
        self.last_response_detail_level = response_detail_level
        return super().call_model(
            task_type,
            document_text,
            user_input,
            model_name_override=model_name_override,
            response_detail_level=response_detail_level,
        )


def test_parse_error_is_normalized() -> None:
    workspace = make_workspace()
    try:
        settings = build_settings(workspace)
        service = FileService(settings=settings, parser=BrokenPdfParser())

        with pytest.raises(ParseError):
            service.save_upload("bad.pdf", b"%PDF-1.4 fake")
    finally:
        cleanup_workspace(workspace)


def test_document_parser_strips_surrogate_codepoints() -> None:
    parser = DocumentParser()

    normalized = parser._normalize_text("正常文本\ud835保留部分")

    assert normalized == "正常文本保留部分"


def test_task_service_still_returns_when_log_write_fails() -> None:
    workspace = make_workspace()
    try:
        settings = build_settings(workspace)
        file_service = FileService(settings=settings)
        task_service = TaskService(
            file_service=file_service,
            model_client=ModelClient(settings=settings),
            log_service=FailingLogService(settings=settings),
        )
        upload = file_service.save_upload("demo.txt", "一段测试内容".encode("utf-8"))

        result = task_service.run_task(
            task_type="ask",
            endpoint="/api/ask",
            file_id=upload.file_id,
            user_input="这段内容说了什么？",
        )

        assert result.result
        assert result.task_type == "ask"
    finally:
        cleanup_workspace(workspace)


def test_log_service_skips_malformed_lines() -> None:
    workspace = make_workspace()
    try:
        settings = build_settings(workspace)
        log_service = LogService(settings=settings)
        log_service.log_file.write_text(
            '{"request_id":"ok","timestamp":"now","endpoint":"/api/ask","task_type":"ask","model_name":"m","success":true,"latency_ms":1,"prompt_chars":1,"output_chars":1}\n'
            '{bad json line}\n',
            encoding="utf-8",
        )

        logs = log_service.list_logs(limit=10)

        assert len(logs) == 1
        assert logs[0]["request_id"] == "ok"
    finally:
        cleanup_workspace(workspace)


def test_log_service_summary_aggregates_metrics() -> None:
    workspace = make_workspace()
    try:
        settings = build_settings(workspace)
        log_service = LogService(settings=settings)
        log_service.log_file.write_text(
            "\n".join(
                [
                    '{"request_id":"1","timestamp":"2026-04-15T01:00:00+00:00","endpoint":"/api/summary","task_type":"summary","model_name":"m1","route_tier":"lite","success":true,"outcome":"answered","latency_ms":100,"prompt_chars":10,"output_chars":20,"token_total":30,"cache_hit":false,"retrieval_status":"coverage","extra":{"citation_count":2}}',
                    '{"request_id":"2","timestamp":"2026-04-15T01:01:00+00:00","endpoint":"/api/ask","task_type":"ask","model_name":"m1","route_tier":"none","response_detail_level":"concise","success":true,"outcome":"refused","latency_ms":400,"prompt_chars":10,"output_chars":15,"token_total":0,"cache_hit":false,"retrieval_status":"no_match","extra":{"citation_count":0}}',
                    '{"request_id":"3","timestamp":"2026-04-15T01:02:00+00:00","endpoint":"/api/summary","task_type":"summary","model_name":"m2","route_tier":"pro","response_detail_level":"detailed","success":false,"outcome":"error","latency_ms":200,"prompt_chars":10,"output_chars":0,"token_total":40,"cache_hit":true,"retrieval_applied":true,"retrieval_status":"matched","error_type":"MODEL_SERVICE_ERROR","extra":{"citation_count":1}}',
                    "{bad json line}",
                ]
            ),
            encoding="utf-8",
        )

        summary = log_service.summarize_logs()

        assert summary["total_requests"] == 3
        assert summary["success_count"] == 2
        assert summary["failure_count"] == 1
        assert summary["cache_hit_count"] == 1
        assert summary["retrieval_applied_count"] == 1
        assert summary["citation_count_sum"] == 3
        assert summary["answered_count"] == 1
        assert summary["refused_count"] == 1
        assert summary["error_count"] == 1
        assert summary["token_total_sum"] == 70
        assert summary["by_task"]["summary"] == 2
        assert summary["by_task"]["ask"] == 1
        assert summary["by_model"]["m1"] == 2
        assert summary["by_model"]["m2"] == 1
        assert summary["by_outcome"]["answered"] == 1
        assert summary["by_outcome"]["refused"] == 1
        assert summary["by_outcome"]["error"] == 1
        assert summary["by_response_detail_level"]["concise"] == 1
        assert summary["by_response_detail_level"]["detailed"] == 1
        assert summary["by_route_tier"]["lite"] == 1
        assert summary["by_route_tier"]["none"] == 1
        assert summary["by_route_tier"]["pro"] == 1
        assert summary["by_retrieval_status"]["coverage"] == 1
        assert summary["by_retrieval_status"]["no_match"] == 1
        assert summary["by_retrieval_status"]["matched"] == 1
        assert summary["error_types"]["MODEL_SERVICE_ERROR"] == 1
    finally:
        cleanup_workspace(workspace)


def test_task_service_uses_cache_for_same_request() -> None:
    workspace = make_workspace()
    try:
        settings = build_settings(workspace)
        file_service = FileService(settings=settings)
        log_service = LogService(settings=settings)
        model_client = CountingModelClient(settings=settings)
        task_service = TaskService(
            file_service=file_service,
            model_client=model_client,
            log_service=log_service,
        )
        upload = file_service.save_upload("demo.txt", "缓存测试内容".encode("utf-8"))

        first = task_service.run_task(
            task_type="summary",
            endpoint="/api/summary",
            file_id=upload.file_id,
            user_input="请总结",
            response_detail_level="concise",
        )
        second = task_service.run_task(
            task_type="summary",
            endpoint="/api/summary",
            file_id=upload.file_id,
            user_input="请总结",
            response_detail_level="concise",
        )

        assert first.cache_hit is False
        assert second.cache_hit is True
        assert model_client.call_count == 1
        assert first.result == second.result
    finally:
        cleanup_workspace(workspace)


def test_task_service_separates_cache_by_response_detail_level() -> None:
    workspace = make_workspace()
    try:
        settings = build_settings(workspace)
        file_service = FileService(settings=settings)
        log_service = LogService(settings=settings)
        model_client = CountingModelClient(settings=settings)
        task_service = TaskService(
            file_service=file_service,
            model_client=model_client,
            log_service=log_service,
        )
        upload = file_service.save_upload("demo.txt", "缓存测试内容".encode("utf-8"))

        concise = task_service.run_task(
            task_type="summary",
            endpoint="/api/summary",
            file_id=upload.file_id,
            user_input="请总结",
            response_detail_level="concise",
        )
        detailed = task_service.run_task(
            task_type="summary",
            endpoint="/api/summary",
            file_id=upload.file_id,
            user_input="请总结",
            response_detail_level="detailed",
        )

        assert concise.response_detail_level == "concise"
        assert detailed.response_detail_level == "detailed"
        assert model_client.call_count == 2
    finally:
        cleanup_workspace(workspace)


def test_task_service_applies_retrieval_for_ask() -> None:
    workspace = make_workspace()
    try:
        settings = build_settings(workspace)
        file_service = FileService(settings=settings)
        task_service = TaskService(
            file_service=file_service,
            model_client=ModelClient(settings=settings),
            log_service=LogService(settings=settings),
        )
        upload = file_service.save_upload(
            "retrieval.md",
            (
                "# 第一部分\n\n这里讨论无关背景信息。\n\n"
                "# 第二部分\n\n第一阶段目标是支持上传文档、摘要、问答和提纲生成。"
            ).encode("utf-8"),
        )

        result = task_service.run_task(
            task_type="ask",
            endpoint="/api/ask",
            file_id=upload.file_id,
            user_input="第一阶段目标是什么？",
        )

        assert result.retrieval_applied is True
        assert result.retrieved_chunk_count >= 1
        assert result.retrieved_pages == [1]
        assert len(result.citations) >= 1
        assert result.citations[0].page_numbers == [1]
        assert result.source_chunks == []
    finally:
        cleanup_workspace(workspace)


def test_task_service_avoids_fake_citations_on_retrieval_miss() -> None:
    workspace = make_workspace()
    try:
        settings = build_settings(workspace)
        file_service = FileService(settings=settings)
        task_service = TaskService(
            file_service=file_service,
            model_client=ModelClient(settings=settings),
            log_service=LogService(settings=settings),
        )
        upload = file_service.save_upload(
            "miss.md",
            "# 文档\n\n这里讨论项目背景和目标。".encode("utf-8"),
        )

        result = task_service.run_task(
            task_type="ask",
            endpoint="/api/ask",
            file_id=upload.file_id,
            user_input="完全不相关的天文问题",
        )

        assert result.outcome == "refused"
        assert result.retrieval_status == "no_match"
        assert result.retrieval_message
        assert result.retrieval_applied is False
        assert result.retrieved_chunk_count == 0
        assert result.citations == []
    finally:
        cleanup_workspace(workspace)


def test_summary_uses_chunk_coverage_context() -> None:
    workspace = make_workspace()
    try:
        settings = build_settings(workspace)
        file_service = FileService(settings=settings)
        model_client = RecordingModelClient(settings=settings)
        task_service = TaskService(
            file_service=file_service,
            model_client=model_client,
            log_service=LogService(settings=settings),
        )
        upload = file_service.save_upload(
            "coverage.md",
            (
                "# 第一章\n\n第一章内容。\n\n"
                "# 第二章\n\n第二章内容。\n\n"
                "# 第三章\n\n第三章内容。\n\n"
                "# 第四章\n\n第四章内容。\n\n"
                "# 第五章\n\n第五章内容。\n\n"
                "# 第六章\n\n第六章内容。"
            ).encode("utf-8"),
        )

        result = task_service.run_task(
            task_type="summary",
            endpoint="/api/summary",
            file_id=upload.file_id,
            user_input="请总结",
        )

        assert result.task_type == "summary"
        assert "【Chunk" in model_client.last_document_text
        assert result.citations == []
        assert len(result.source_chunks) >= 1
    finally:
        cleanup_workspace(workspace)


def test_summary_planner_responds_to_instruction_intent() -> None:
    workspace = make_workspace()
    try:
        settings = build_settings(workspace)
        file_service = FileService(settings=settings)
        model_client = RecordingModelClient(settings=settings)
        task_service = TaskService(
            file_service=file_service,
            model_client=model_client,
            log_service=LogService(settings=settings),
        )
        upload = file_service.save_upload(
            "intent.md",
            (
                "# 背景\n\n"
                + ("这是研究背景。" * 80)
                + "\n\n# 数据集\n\n"
                + ("这里介绍数据集构成与标注方式。" * 80)
                + "\n\n# 方法\n\n"
                + ("这里重点介绍方法设计与实现。" * 80)
                + "\n\n# 消融实验\n\n"
                + ("这里介绍消融实验设置与比较结果。" * 80)
                + "\n\n# 实验结果\n\n"
                + ("这里重点介绍实验结果和性能表现。" * 80)
                + "\n\n# 误差分析\n\n"
                + ("这里分析模型误差与失败案例。" * 80)
                + "\n\n# 结论\n\n"
                + ("这里给出最终结论。" * 50)
                + "\n\n# 附录\n\n"
                + ("这里是补充说明与附录内容。" * 60)
            ).encode("utf-8"),
        )

        task_service.run_task(
            task_type="summary",
            endpoint="/api/summary",
            file_id=upload.file_id,
            user_input="请重点总结实验结果",
        )
        experiment_text = model_client.last_document_text

        task_service.run_task(
            task_type="summary",
            endpoint="/api/summary",
            file_id=upload.file_id,
            user_input="请重点总结方法部分",
        )
        method_text = model_client.last_document_text

        assert "实验结果" in experiment_text
        assert "方法设计" in method_text
        assert experiment_text != method_text
    finally:
        cleanup_workspace(workspace)


def test_summary_source_chunks_are_cleaned_for_display() -> None:
    workspace = make_workspace()
    try:
        settings = build_settings(workspace)
        file_service = FileService(settings=settings)
        task_service = TaskService(
            file_service=file_service,
            model_client=ModelClient(settings=settings),
            log_service=LogService(settings=settings),
        )
        upload = file_service.save_upload(
            "cleaning.md",
            (
                "任 任 任 任务 务 务报 报 报告 告 告\n\n"
                "第二十三届中国计算语言学大会论文集\n\n"
                "这里是一段正常的研究说明，应该保留在来源片段里。"
            ).encode("utf-8"),
        )

        result = task_service.run_task(
            task_type="summary",
            endpoint="/api/summary",
            file_id=upload.file_id,
            user_input="请总结",
        )

        assert result.source_chunks
        snippet = result.source_chunks[0].snippet
        assert "任 任 任" not in snippet
        assert "第二十三届中国计算语言学大会论文集" not in snippet
        assert "正常的研究说明" in snippet
    finally:
        cleanup_workspace(workspace)


def test_task_service_uses_task_tier_route_when_configured() -> None:
    workspace = make_workspace()
    try:
        settings = build_settings(
            workspace,
            model_lite="lite-model",
            model_pro="pro-model",
        )
        file_service = FileService(settings=settings)
        model_client = RecordingModelClient(settings=settings)
        task_service = TaskService(
            file_service=file_service,
            model_client=model_client,
            log_service=LogService(settings=settings),
        )
        upload = file_service.save_upload("demo.md", "# 标题\n\n内容".encode("utf-8"))

        summary_result = task_service.run_task(
            task_type="summary",
            endpoint="/api/summary",
            file_id=upload.file_id,
            user_input="请总结",
        )
        ask_result = task_service.run_task(
            task_type="ask",
            endpoint="/api/ask",
            file_id=upload.file_id,
            user_input="标题是什么？",
        )

        assert summary_result.route_tier == "lite"
        assert summary_result.route_model == "lite-model"
        assert ask_result.route_tier == "pro"
        assert ask_result.route_model == "pro-model"
    finally:
        cleanup_workspace(workspace)


def test_chunk_ids_are_stable_for_same_text() -> None:
    parsed_document = ParsedDocument(
        file_type="md",
        text="# 标题\n\n第一段\n\n第二段",
        page_count=1,
        pages=[
            ParsedPage(
                page_number=1,
                text="# 标题\n\n第一段\n\n第二段",
                char_count=len("# 标题\n\n第一段\n\n第二段"),
            )
        ],
    )
    service = ChunkService()

    first = service.build_chunks(parsed_document)
    second = service.build_chunks(parsed_document)

    assert [chunk.chunk_id for chunk in first.chunks] == [chunk.chunk_id for chunk in second.chunks]


def test_chunk_service_assigns_stable_source_order() -> None:
    parsed_document = ParsedDocument(
        file_type="md",
        text="# 标题\n\n第一段\n\n第二段\n\n第三段",
        page_count=1,
        pages=[
            ParsedPage(
                page_number=1,
                text="# 标题\n\n第一段\n\n第二段\n\n第三段",
                char_count=len("# 标题\n\n第一段\n\n第二段\n\n第三段"),
            )
        ],
    )
    service = ChunkService(target_chunk_chars=6, min_chunk_chars=1, long_text_step=6)

    chunked = service.build_chunks(parsed_document)

    assert [chunk.chunk_index for chunk in chunked.chunks] == list(range(chunked.chunk_count))


def test_retrieval_service_handles_filler_words_and_title_bonus() -> None:
    parsed_document = ParsedDocument(
        file_type="md",
        text="# 项目目标\n\n第一阶段目标是支持上传文档、摘要、问答和提纲生成。\n\n# 背景\n\n其他背景信息。",
        page_count=1,
        pages=[
            ParsedPage(
                page_number=1,
                text="# 项目目标\n\n第一阶段目标是支持上传文档、摘要、问答和提纲生成。\n\n# 背景\n\n其他背景信息。",
                char_count=len("# 项目目标\n\n第一阶段目标是支持上传文档、摘要、问答和提纲生成。\n\n# 背景\n\n其他背景信息。"),
            )
        ],
    )
    chunked = ChunkService().build_chunks(parsed_document)
    retrieval = RetrievalService()

    selected = retrieval.retrieve("请问这个项目第一阶段要做什么？", chunked)

    assert selected
    assert "第一阶段目标" in selected[0].text


def test_retrieval_normalize_query_preserves_english_tokens() -> None:
    retrieval = RetrievalService()

    normalized = retrieval._normalize_query("what is the architecture")

    assert normalized == "architecture"


def test_retrieval_skips_oversized_chunk_and_continues() -> None:
    retrieval = RetrievalService(top_k=2, max_context_chars=60, min_score=0.0)
    chunked = ChunkedDocument(
        file_type="md",
        page_count=1,
        chunk_count=3,
        chunks=[
            ParsedChunk(
                chunk_id="big",
                chunk_index=0,
                page_numbers=[1],
                text="方法 " * 80,
                char_count=len("方法 " * 80),
            ),
            ParsedChunk(
                chunk_id="small-1",
                chunk_index=1,
                page_numbers=[1],
                text="这里介绍方法设计。",
                char_count=len("这里介绍方法设计。"),
            ),
            ParsedChunk(
                chunk_id="small-2",
                chunk_index=2,
                page_numbers=[1],
                text="这里总结方法优点。",
                char_count=len("这里总结方法优点。"),
            ),
        ],
    )

    selected = retrieval.retrieve("方法", chunked)

    assert [chunk.chunk_id for chunk in selected] == ["small-1", "small-2"]
