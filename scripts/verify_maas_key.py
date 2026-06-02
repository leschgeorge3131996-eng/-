"""验证 .env 里的无问芯穹 MaaS key 是否可用 —— 只输出状态，永不回显 key 本体。

用途：换号（如换成代金券账号）后，确认 ① key 通 ② 模型有权限 ③ 能拿到真实
``platform_request_id``。脚本只打印 key 的长度，绝不打印 key 字符。

跑法（仓库根）：
    .venv/Scripts/python.exe scripts/verify_maas_key.py
"""
from __future__ import annotations

import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
except Exception:
    pass

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "backend"))

from app.core.config import get_settings  # noqa: E402
from app.services.model_client import ModelClient  # noqa: E402


def main() -> int:
    settings = get_settings()
    print("=" * 60)
    print("MaaS key 验证（只看状态，不回显 key 本体）")
    print("=" * 60)
    print(f"base_url        : {settings.wuqiong_base_url or '(空!)'}")
    print(f"api_key         : {'已填，长度 ' + str(len(settings.wuqiong_api_key)) if settings.wuqiong_api_key else '(空!)'}")
    print(f"use_mock_model  : {settings.use_mock_model}")
    print(f"QA 模型         : {settings.model_qa}")
    print(f"summary/outline : {settings.model_summary} / {settings.model_outline}")
    print("-" * 60)

    if not settings.wuqiong_base_url or not settings.wuqiong_api_key:
        print("[FAIL] base_url 或 api_key 为空 —— .env 没填全。")
        return 1
    if settings.use_mock_model:
        print("[FAIL] use_mock_model=True —— 会走假调用。把 .env 的 USE_MOCK_MODEL 设为 false。")
        return 1

    print("发起一次最小真实调用（task=ask，极短文档 + 问题，耗 token 极少）…")
    client = ModelClient(settings)
    try:
        result = client.call_model(
            task_type="ask",
            document_text="研答通是一个引用可核验的文档问答系统，它的每条答案都能回链到 PDF 原文证据。",
            user_input="这个系统的答案有什么特点？",
        )
    except Exception as exc:  # noqa: BLE001
        print(f"[FAIL] 调用抛异常：{type(exc).__name__}: {exc}")
        print("       常见原因：key 错(401)、模型没开通/无权限(404)、网络或 base_url 错。")
        return 1

    if result.model_name.startswith("mock::"):
        print(f"[FAIL] 返回的是 mock（model_name={result.model_name}）—— 没真调云端。")
        return 1

    rid = result.platform_request_id
    print("[OK] 真实调用成功")
    print(f"     模型            : {result.model_name}")
    print(f"     平台 request_id : {rid or '(未返回 id；不影响可用，但决赛对账更想要 id)'}")
    if result.token_usage:
        print(
            f"     token           : prompt={result.token_usage.prompt_tokens} "
            f"completion={result.token_usage.completion_tokens} "
            f"total={result.token_usage.total_tokens}"
        )
    snippet = (result.content or "").strip().replace("\n", " ")[:80]
    print(f"     回答片段        : {snippet}…")
    print("-" * 60)
    print("结论：key 可用、模型有权限、能拿到真实调用记录。")
    if rid:
        print(f"→ 拿这个 request_id 去无问芯穹控制台核对：这笔是否计到代金券号。")
    print("→ 解锁：H2 智能体真多轮日志 / H4 带真实平台 id 的 predeploy。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
