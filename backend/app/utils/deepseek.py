"""DeepSeek API client."""
import os
from dataclasses import dataclass
from typing import Optional

import httpx

DEEPSEEK_BASE_URL = "https://api.deepseek.com"
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")


@dataclass
class DeepSeekConfig:
    model: str = "deepseek-chat"
    temperature: float = 0.8
    max_tokens: int = 2048
    timeout: float = 30.0


class DeepSeekError(Exception):
    """DeepSeek API 调用异常."""

    def __init__(self, message: str, status_code: Optional[int] = None):
        super().__init__(message)
        self.status_code = status_code


class DeepSeekClient:
    """DeepSeek API 客户端."""

    def __init__(self, config: Optional[DeepSeekConfig] = None):
        self.config = config or DeepSeekConfig()
        if not DEEPSEEK_API_KEY:
            raise DeepSeekError(
                "DEEPSEEK_API_KEY 环境变量未设置。"
                "请在 .env 文件中设置或通过环境变量导出。"
            )

    @property
    def _headers(self) -> dict:
        return {
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
            "Content-Type": "application/json",
        }

    async def chat(
        self,
        system_prompt: str,
        user_prompt: str,
    ) -> str:
        """发送 chat completion 请求，返回响应文本."""
        payload = {
            "model": self.config.model,
            "temperature": self.config.temperature,
            "max_tokens": self.config.max_tokens,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        }

        async with httpx.AsyncClient(timeout=self.config.timeout) as client:
            try:
                response = await client.post(
                    f"{DEEPSEEK_BASE_URL}/chat/completions",
                    headers=self._headers,
                    json=payload,
                )
            except httpx.TimeoutException:
                raise DeepSeekError("DeepSeek API 请求超时", status_code=504)
            except httpx.RequestError as e:
                raise DeepSeekError(f"网络请求失败: {e}", status_code=500)

        if response.status_code != 200:
            raise DeepSeekError(
                f"DeepSeek API 返回错误 ({response.status_code}): {response.text}",
                status_code=response.status_code,
            )

        data = response.json()
        try:
            return data["choices"][0]["message"]["content"]
        except (KeyError, IndexError) as e:
            raise DeepSeekError(f"DeepSeek 响应格式异常: {e}", status_code=502)
