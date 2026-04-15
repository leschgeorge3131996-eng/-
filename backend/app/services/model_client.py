from __future__ import annotations

import json
import textwrap
import time
import urllib.error
import urllib.request

from ..core.config import Settings, get_settings
from ..core.exceptions import ModelServiceError
from ..schemas.task import ModelResult, TaskType, TokenUsage


class ModelClient:
    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or get_settings()

    def call_model(
        self,
        task_type: TaskType,
        document_text: str,
        user_input: str | None = None,
    ) -> ModelResult:
        truncated_text = document_text[: self.settings.max_document_chars]
        context_truncated = len(truncated_text) < len(document_text)
        model_name = self.resolve_model_name(task_type)
        prompt_chars = len(truncated_text) + len(user_input or "")

        if self.settings.use_mock_model or not self._has_real_model_config():
            content = self._mock_response(task_type, truncated_text, user_input)
            return ModelResult(
                content=content,
                model_name=f"mock::{model_name}",
                prompt_chars=prompt_chars,
                output_chars=len(content),
                token_usage=None,
                context_truncated=context_truncated,
            )

        payload = {
            "model": model_name,
            "messages": self._build_messages(task_type, truncated_text, user_input),
            "temperature": 0.2,
        }
        response_json = self._call_openai_compatible_api(payload)
        content = self._extract_content(response_json)
        usage = response_json.get("usage") or {}

        return ModelResult(
            content=content,
            model_name=model_name,
            prompt_chars=prompt_chars,
            output_chars=len(content),
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

    def _has_real_model_config(self) -> bool:
        return bool(self.settings.wuqiong_base_url and self.settings.wuqiong_api_key)

    def _build_messages(
        self,
        task_type: TaskType,
        document_text: str,
        user_input: str | None,
    ) -> list[dict[str, str]]:
        if task_type == "ask":
            system_prompt = "你是文档问答助手。只能依据给定文档回答，回答要准确、简洁、结构清晰。"
            user_prompt = textwrap.dedent(
                f"""
                文档内容如下：
                {document_text}

                用户问题：
                {user_input or "请基于文档回答问题。"}
                """
            ).strip()
        elif task_type == "summary":
            system_prompt = "你是文档摘要助手。请输出结构化摘要，突出关键信息、核心结论和可行动建议。"
            user_prompt = textwrap.dedent(
                f"""
                文档内容如下：
                {document_text}

                附加要求：
                {user_input or "请给出一份简明摘要。"}
                """
            ).strip()
        else:
            system_prompt = "你是提纲生成助手。请基于文档生成清晰、可展示的层级提纲。"
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
                break
            except TimeoutError as exc:
                last_error = ModelServiceError("云端模型调用超时。")
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
    ) -> str:
        preview = document_text[:800].strip()
        lines = [line.strip() for line in preview.splitlines() if line.strip()]
        points = lines[:5] if lines else ["文档内容较短，建议上传更完整内容。"]

        if task_type == "ask":
            question = user_input or "未提供问题"
            return (
                "【Mock 模型返回】\n"
                f"问题：{question}\n\n"
                "基于当前文档可见内容，相关信息如下：\n"
                + "\n".join(f"- {point}" for point in points)
            )

        if task_type == "summary":
            instruction = user_input or "默认摘要"
            return (
                "【Mock 模型返回】\n"
                f"摘要要求：{instruction}\n\n"
                "摘要：\n"
                + "\n".join(f"- {point}" for point in points[:3])
            )

        instruction = user_input or "默认提纲"
        rendered = "\n".join(
            f"{index}. {point}" for index, point in enumerate(points[:4], start=1)
        )
        return f"【Mock 模型返回】\n提纲要求：{instruction}\n\n{rendered}"
