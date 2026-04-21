"""AzureSearchService — IKBSearchService implementation using Azure AI Search (hybrid)."""
from __future__ import annotations

from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.models import VectorizedQuery

from src.domain.entities.kb_chunk import KBChunk
from src.domain.ports.kb_search_port import IKBSearchService
from src.domain.value_objects.user_role import UserRole

_SEMANTIC_CONFIG = "it-helpdesk-semantic"


class AzureSearchService(IKBSearchService):
    def __init__(
        self,
        endpoint: str,
        api_key: str,
        index_name: str,
        embedding_fn: "Callable[[str], list[float]] | None" = None,
    ) -> None:
        self._client = SearchClient(
            endpoint=endpoint,
            index_name=index_name,
            credential=AzureKeyCredential(api_key),
        )
        self._embedding_fn = embedding_fn  # injected for vector search

    def search(
        self,
        query: str,
        user_role: UserRole,
        top_k: int = 5,
        doc_versions: list[str] | None = None,
    ) -> list[KBChunk]:
        # Build RBAC filter
        if user_role == UserRole.IT_ADMIN:
            rbac_filter = None  # no restriction — can see all documents
        else:
            rbac_filter = "access_role eq 'public'"

        # Add optional doc_versions filter (for version comparison queries)
        version_filter = None
        if doc_versions:
            version_clauses = " or ".join(
                f"doc_version eq '{v}'" for v in doc_versions
            )
            version_filter = f"({version_clauses})"

        # Combine filters
        combined_filter = " and ".join(
            f for f in [rbac_filter, version_filter] if f
        ) or None

        # Build optional vector query
        vector_queries = []
        if self._embedding_fn:
            vector = self._embedding_fn(query)
            vector_queries = [
                VectorizedQuery(
                    vector=vector,
                    k_nearest_neighbors=top_k,
                    fields="content_vector",
                )
            ]

        results = self._client.search(
            search_text=query,
            filter=combined_filter,
            top=top_k,
            vector_queries=vector_queries or None,
            query_type="semantic" if not vector_queries else "simple",
            semantic_configuration_name=_SEMANTIC_CONFIG if not vector_queries else None,
            select=["id", "content", "source_file", "doc_version", "page_number", "access_role"],
        )

        chunks: list[KBChunk] = []
        for r in results:
            score = r.get("@search.score") or r.get("@search.reranker_score") or 0.0
            chunks.append(
                KBChunk(
                    chunk_id=r["id"],
                    content=r["content"],
                    source_file=r["source_file"],
                    doc_version=r["doc_version"],
                    page_number=r.get("page_number", 0),
                    access_role=r.get("access_role", "public"),
                    score=float(score),
                )
            )
        return chunks
