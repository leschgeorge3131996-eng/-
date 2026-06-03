"""bbox 证据回链端到端量化（产品立身点的证据腿）。

只读、离线（系统作答可命中缓存）。对固定题集逐条跑真实 ask，统计系统产出的 citation
里有多少**成功把证据 quote 定位到 PDF 页面的行级 bbox**（vs 回退到无行级高亮）。

诚实护栏：
- 指标是"**行级可定位率**"（quote 能否落到 ≥1 行），不是"命中正确行的准确率"——本库无人工
  标注的 gold 行；要声称"定位到正确行"需另做人工抽查并分开列。
- "回退触发率"（未匹配到行）本身是有用的诚实信号，不藏。
- 零改 bbox_matcher / 校验 / 回链 / 拒答任何核心，仅事后测量。

跑法：.venv/Scripts/python.exe scripts/bbox_grounding_eval.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from backend.app.core.config import get_settings  # noqa: E402
from backend.app.services.auth_service import AuthService  # noqa: E402
from backend.app.services.file_service import FileService  # noqa: E402
from backend.app.services.log_service import LogService  # noqa: E402
from backend.app.services.model_client import ModelClient  # noqa: E402
from backend.app.services.task_service import TaskService  # noqa: E402

MANIFEST = ROOT / "evidence/materials/EXTENDED_EVAL_V1.json"


def main() -> int:
    s = get_settings()
    if s.use_mock_model or not (s.wuqiong_base_url and s.wuqiong_api_key):
        print("[FAIL] 需要真实 MaaS 配置（.env）。")
        return 1
    auth = AuthService(settings=s)
    fs = FileService(settings=s)
    ls = LogService(settings=s)
    mc = ModelClient(settings=s)
    ts = TaskService(file_service=fs, model_client=mc, log_service=ls)
    sess = auth.create_session("alpha-demo").session.session_id

    d = json.loads(MANIFEST.read_text(encoding="utf-8"))
    uploads: dict[str, object] = {}
    total_cases = 0
    cited_cases = 0
    total_citations = 0
    located_citations = 0  # bbox_regions 非空（≥1 行）
    total_lines = 0
    per_doc: dict[str, list[int]] = {}

    for it in d["items"]:
        dp = it["document_path"]
        if dp not in uploads:
            uploads[dp] = fs.save_upload(Path(dp).name, (ROOT / dp).read_bytes(), owner_session_id=sess)
        up = uploads[dp]
        for p in it.get("prompts", []):
            if p.get("kind") == "refusal":
                continue
            total_cases += 1
            try:
                r = ts.run_task(
                    task_type="ask", endpoint="/api/ask", file_id=up.file_id,
                    session_id=sess, document_access_token=up.access_token,
                    user_input=p["text"], response_detail_level="balanced",
                )
            except Exception:
                continue
            cits = getattr(r, "citations", []) or []
            if cits:
                cited_cases += 1
            for c in cits:
                total_citations += 1
                nlines = len(getattr(c, "bbox_regions", []) or [])
                if nlines >= 1:
                    located_citations += 1
                    total_lines += nlines
                per_doc.setdefault(it["doc_id"], [0, 0])
                per_doc[it["doc_id"]][0] += 1
                per_doc[it["doc_id"]][1] += 1 if nlines >= 1 else 0

    located_rate = located_citations / total_citations if total_citations else 0
    avg_lines = total_lines / located_citations if located_citations else 0
    fallback_rate = 1 - located_rate

    print("=" * 60)
    print("bbox 证据回链量化（行级可定位率）")
    print("=" * 60)
    print(f"答题用例           : {total_cases}（有 citation 的 {cited_cases}）")
    print(f"总 citation         : {total_citations}")
    print(f"行级可定位（≥1 行） : {located_citations}  → **可定位率 {located_rate*100:.1f}%**")
    print(f"回退（无行级匹配）  : {total_citations - located_citations}  → 回退率 {fallback_rate*100:.1f}%")
    print(f"已定位条平均覆盖行数: {avg_lines:.1f}")
    print("-" * 60)
    print("按文档（可定位/总）:")
    for did, (tot, loc) in per_doc.items():
        print(f"  {did}: {loc}/{tot}")
    print("-" * 60)
    print("诚实口径：'可定位率'=quote 能否落到 ≥1 行；非'命中正确行准确率'（无人工 gold 行）。")
    print("回退率本身是诚实信号；要声称'定位到正确行'需另做人工抽查并分开列。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
