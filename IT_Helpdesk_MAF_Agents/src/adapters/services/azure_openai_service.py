"""AzureOpenAIService — ILLMService implementation using Azure OpenAI GPT-4o."""
from __future__ import annotations

from openai import AzureOpenAI

from src.domain.ports.llm_port import ILLMService


class AzureOpenAIService(ILLMService):
    def __init__(
        self,
        endpoint: str,
        api_key: str,
        deployment: str,
        api_version: str = "2024-02-01",
    ) -> None:
        self._client = AzureOpenAI(
            azure_endpoint=endpoint,
            api_key=api_key,
            api_version=api_version,
        )
        self._deployment = deployment

    def complete(self, messages: list[dict]) -> str:
        response = self._client.chat.completions.create(
            model=self._deployment,
            messages=messages,
            temperature=0.2,
            max_tokens=1024,
        )
        return response.choices[0].message.content or ""
