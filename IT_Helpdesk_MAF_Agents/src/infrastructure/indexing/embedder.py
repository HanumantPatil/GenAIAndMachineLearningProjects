"""Embedder — generates dense vectors using Azure OpenAI text-embedding-3-large."""
from __future__ import annotations

from openai import AzureOpenAI


class Embedder:
    def __init__(
        self,
        endpoint: str,
        api_key: str,
        deployment: str = "text-embedding-3-large",
        api_version: str = "2024-02-01",
        batch_size: int = 16,
    ) -> None:
        self._client = AzureOpenAI(
            azure_endpoint=endpoint, api_key=api_key, api_version=api_version
        )
        self._deployment = deployment
        self._batch_size = batch_size

    def embed_documents(self, documents: list[dict]) -> list[dict]:
        """Add *content_vector* to each document in-place and return the list."""
        texts = [doc["content"] for doc in documents]
        for i in range(0, len(texts), self._batch_size):
            batch = texts[i : i + self._batch_size]
            response = self._client.embeddings.create(input=batch, model=self._deployment)
            for j, emb in enumerate(response.data):
                documents[i + j]["content_vector"] = emb.embedding
        return documents

    def embed_query(self, query: str) -> list[float]:
        response = self._client.embeddings.create(input=[query], model=self._deployment)
        return response.data[0].embedding
