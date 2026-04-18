from __future__ import annotations

import json
import re
import textwrap
import time
import urllib.error
import urllib.request
from dataclasses import dataclass

from ..core.config import Settings, get_settings
from ..core.exceptions import ModelServiceError
from ..schemas.task import ModelResult, ResponseDetailLevel, TaskType, TokenUsage


@dataclass(slots=True)
class RouteDecision:
    model_name: str
    route_tier: str
    route_reason: str


class ModelClient:
    complex_keywords = (
        "对比",
        "原因",
        "风险",
        "方案",
        "结合全文",
        "深入分析",
        "答辩",
        "compare",
        "analysis",
        "risk",
        "reason",
    )

    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or get_settings()

    def call_model(
        self,
        task_type: TaskType,
        document_text: str,
        user_input: str | None = None,
        model_name_override: str | None = None,
        response_detail_level: ResponseDetailLevel = "balanced",
    ) -> ModelResult:
        source_document_chars = len(document_text)
        truncated_text = document_text[: self.settings.max_document_chars]
        context_truncated = len(truncated_text) < len(document_text)
        used_document_chars = len(truncated_text)
        truncation_message = None
        if context_truncated:
            truncation_message = (
                f"文档原始长度为 {source_document_chars} 字符，本次请求仅发送前 "
                f"{used_document_chars} 字符到模型。"
            )
        model_name = model_name_override or self.resolve_model_name(task_type)
        prompt_chars = len(truncated_text) + len(user_input or "")

        if self.settings.use_mock_model or not self._has_real_model_config():
            content = self._mock_response(
                task_type,
                truncated_text,
                user_input,
                response_detail_level=response_detail_level,
            )
            return ModelResult(
                content=content,
                model_name=f"mock::{model_name}",
                prompt_chars=prompt_chars,
                output_chars=len(content),
                source_document_chars=source_document_chars,
                used_document_chars=used_document_chars,
                truncation_message=truncation_message,
                token_usage=None,
                context_truncated=context_truncated,
            )

        payload = {
            "model": model_name,
            "messages": self._build_messages(
                task_type,
                truncated_text,
                user_input,
                response_detail_level=response_detail_level,
            ),
            "temperature": 0 if task_type == "ask" else 0.2,
        }
        response_json = self._call_openai_compatible_api(payload)
        content = self._extract_content(response_json)
        usage = response_json.get("usage") or {}

        return ModelResult(
            content=content,
            model_name=model_name,
            prompt_chars=prompt_chars,
            output_chars=len(content),
            source_document_chars=source_document_chars,
            used_document_chars=used_document_chars,
            truncation_message=truncation_message,
            token_usage=TokenUsage(
                prompt_tokens=usage.get("prompt_tokens"),
                completion_tokens=usage.get("completion_tokens"),
                total_tokens=usage.get("total_tokens"),
            ),
            context_truncated=context_truncated,
        )

    def resolve_model_name(self, task_type: TaskType) -> str:
        if task_type == "ask":
            return self.settings.model_qa
        if task_type == "summary":
            return self.settings.model_summary
        return self.settings.model_outline

    def resolve_route(
        self,
        *,
        task_type: TaskType,
        user_input: str | None = None,
        source_document_chars: int = 0,
    ) -> RouteDecision:
        normalized_input = (user_input or "").lower()
        has_explicit_route_models = bool(self.settings.model_lite and self.settings.model_pro)

        if has_explicit_route_models:
            if task_type == "ask":
                return RouteDecision(
                    model_name=self.settings.model_pro,
                    route_tier="pro",
                    route_reason="task_default_ask",
                )

            if (
                source_document_chars >= self.settings.route_upgrade_chars
                or any(keyword in normalized_input for keyword in self.complex_keywords)
            ):
                return RouteDecision(
                    model_name=self.settings.model_pro,
                    route_tier="pro",
                    route_reason="long_doc_or_complex_instruction",
                )

            return RouteDecision(
                model_name=self.settings.model_lite,
                route_tier="lite",
                route_reason=f"default_{task_type}_lite",
            )

        return RouteDecision(
            model_name=self.resolve_model_name(task_type),
            route_tier="task_specific",
            route_reason=f"configured_{task_type}_model",
        )

    def _has_real_model_config(self) -> bool:
        return bool(self.settings.wuqiong_base_url and self.settings.wuqiong_api_key)

    def _build_messages(
        self,
        task_type: TaskType,
        document_text: str,
        user_input: str | None,
        *,
        response_detail_level: ResponseDetailLevel,
    ) -> list[dict[str, str]]:
        detail_instruction = self._detail_instruction(response_detail_level, task_type)
        if task_type == "ask":
            system_prompt = (
                "你是文档问答助手。只能依据给定文档回答，回答要准确、结构清晰。"
                "你必须只从给定的 Chunk 中选取你实际使用的证据块，并严格返回 JSON。"
                "Return at least one evidence_quotes item. Each quote must be copied verbatim "
                "from the corresponding chunk as one contiguous span."
                f"{detail_instruction}"
            )
            user_prompt = textwrap.dedent(
                f"""
                文档内容如下：
                {document_text}

                用户问题：
                {user_input or "请基于文档回答问题。"}

                请只返回一个 JSON 对象，不要输出额外解释，格式如下：
                {{
                  "answer": "你的最终回答",
                  "used_chunk_ids": ["实际使用的 chunk_id"],
                  "evidence_quotes": [
                    {{
                      "chunk_id": "实际使用的 chunk_id",
                      "quote": "required: copy one contiguous evidence span verbatim from the chunk"
                    }}
                  ]
                }}
                """
            ).strip()
        elif task_type == "summary":
            system_prompt = (
                "你是文档摘要助手。请输出结构化摘要，突出关键信息、核心结论和可行动建议。"
                f"{detail_instruction}"
            )
            user_prompt = textwrap.dedent(
                f"""
                文档内容如下：
                {document_text}

                附加要求：
                {user_input or "请给出一份简明摘要。"}
                """
            ).strip()
        else:
            system_prompt = (
                "你是提纲生成助手。请基于文档生成清晰、可展示的层级提纲。"
                f"{detail_instruction}"
            )
            user_prompt = textwrap.dedent(
                f"""
                文档内容如下：
                {document_text}

                附加要求：
                {user_input or "请给出一份适合汇报或答辩的提纲。"}
                """
            ).strip()

        return [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

    def _detail_instruction(
        self,
        response_detail_level: ResponseDetailLevel,
        task_type: TaskType,
    ) -> str:
        if response_detail_level == "concise":
            if task_type == "outline":
                return " 输出尽量精炼，层级不要过深，每一项只保留必要信息。"
            return " 输出尽量精炼，优先给关键结论，不展开冗余说明。"
        if response_detail_level == "detailed":
            if task_type == "outline":
                return " 输出更详细的层级提纲，补充每页重点和展开方向。"
            return " 输出更详细，适当补充背景、方法、依据和展开说明。"
        return " 输出保持适中篇幅，兼顾完整性和可读性。"

    def _call_openai_compatible_api(self, payload: dict) -> dict:
        url = self._resolve_chat_url()
        headers = {
            "Authorization": f"Bearer {self.settings.wuqiong_api_key}",
            "Content-Type": "application/json",
        }
        last_error: ModelServiceError | None = None

        for attempt in range(3):
            request = urllib.request.Request(
                url,
                data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
                headers=headers,
                method="POST",
            )

            try:
                with urllib.request.urlopen(
                    request,
                    timeout=self.settings.request_timeout_seconds,
                ) as response:
                    raw = response.read().decode("utf-8")
            except urllib.error.HTTPError as exc:
                error_body = exc.read().decode("utf-8", errors="ignore")
                if exc.code == 429 and attempt < 2 and self._is_burst_limit_error(error_body):
                    time.sleep(2 * (attempt + 1))
                    continue

                if exc.code == 429 and self._is_burst_limit_error(error_body):
                    raise ModelServiceError(
                        "请求过快，触发了火山方舟限流。请等待 10 到 30 秒后重试。",
                        details={"response": error_body},
                    ) from exc

                raise ModelServiceError(
                    f"云端模型调用失败，HTTP {exc.code}",
                    details={"response": error_body},
                ) from exc
            except urllib.error.URLError as exc:
                last_error = ModelServiceError(
                    "云端模型调用失败，请检查网络、Base URL 或证书配置。",
                    details={"reason": str(exc.reason)},
                )
                if attempt < 2 and self._is_retryable_network_error(str(exc.reason)):
                    time.sleep(2 * (attempt + 1))
                    continue
                break
            except TimeoutError:
                last_error = ModelServiceError("云端模型调用超时。")
                if attempt < 2:
                    time.sleep(2 * (attempt + 1))
                    continue
                break

            try:
                return json.loads(raw)
            except json.JSONDecodeError as exc:
                raise ModelServiceError(
                    "云端模型返回了无法解析的 JSON。",
                    details={"response": raw[:1000]},
                ) from exc

        if last_error is not None:
            raise last_error

        raise ModelServiceError("云端模型调用失败，达到最大重试次数。")

    def _is_burst_limit_error(self, error_body: str) -> bool:
        try:
            payload = json.loads(error_body)
        except json.JSONDecodeError:
            return False

        error = payload.get("error") or {}
        return error.get("code") == "RequestBurstTooFast"

    def _is_retryable_network_error(self, reason: str) -> bool:
        normalized = reason.lower()
        retryable_markers = (
            "timed out",
            "timeout",
            "unexpected eof",
            "temporarily unavailable",
            "connection reset",
            "connection aborted",
            "eof occurred in violation of protocol",
        )
        return any(marker in normalized for marker in retryable_markers)

    def _resolve_chat_url(self) -> str:
        if self.settings.wuqiong_base_url.endswith("/chat/completions"):
            return self.settings.wuqiong_base_url
        return f"{self.settings.wuqiong_base_url}/chat/completions"

    def _extract_content(self, response_json: dict) -> str:
        choices = response_json.get("choices") or []
        if choices:
            message = choices[0].get("message") or {}
            content = message.get("content")
            if isinstance(content, list):
                parts = [item.get("text", "") for item in content if isinstance(item, dict)]
                text = "\n".join(part for part in parts if part)
                return text.strip()
            if isinstance(content, str):
                return content.strip()

        raise ModelServiceError(
            "云端模型返回结构不符合预期。",
            details={"response_keys": list(response_json.keys())},
        )

    def _mock_response(
        self,
        task_type: TaskType,
        document_text: str,
        user_input: str | None,
        response_detail_level: ResponseDetailLevel = "balanced",
    ) -> str:
        preview = document_text[:800].strip()
        lines = [line.strip() for line in preview.splitlines() if line.strip()]
        points = lines[:5] if lines else ["文档内容较短，建议上传更完整内容。"]
        if response_detail_level == "concise":
            max_points = 2
        elif response_detail_level == "detailed":
            max_points = 5
        else:
            max_points = 3

        if task_type == "ask":
            question = user_input or "未提供问题"
            chunk_ids = re.findall(r"【Chunk ([^|]+) \| Pages [^】]+】", document_text)
            used_chunk_ids = chunk_ids[: min(2, len(chunk_ids))]
            evidence_quotes = [line[:60] for line in lines[: min(2, len(lines))]]
            return (
                json.dumps(
                    {
                        "answer": "；".join(points[:max_points]),
                        "used_chunk_ids": used_chunk_ids,
                        "evidence_quotes": [
                            {"chunk_id": used_chunk_ids[0], "quote": quote}
                            for quote in evidence_quotes
                        ]
                        if used_chunk_ids
                        else [],
                        "question": question,
                    },
                    ensure_ascii=False,
                )
            )

        if task_type == "summary":
            instruction = user_input or "默认摘要"
            return (
                "【Mock 模型返回】\n"
                f"摘要要求：{instruction}\n\n"
                "摘要：\n"
                + "\n".join(f"- {point}" for point in points[:max_points])
            )

        instruction = user_input or "默认提纲"
        rendered = "\n".join(
            f"{index}. {point}" for index, point in enumerate(points[:max(3, max_points)], start=1)
        )
        return f"【Mock 模型返回】\n提纲要求：{instruction}\n\n{rendered}"
