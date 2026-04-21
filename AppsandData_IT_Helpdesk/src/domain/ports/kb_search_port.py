"""IKBSearchService port — abstract interface for knowledge base retrieval."""
from abc import ABC, abstractmethod

from src.domain.entities.kb_chunk import KBChunk
from src.domain.value_objects.user_role import UserRole


class IKBSearchService(ABC):
    @abstractmethod
    def search(
        self,
        query: str,
        user_role: UserRole,
        top_k: int = 5,
        doc_versions: list[str] | None = None,
    ) -> list[KBChunk]:
        """
        Perform hybrid (semantic + keyword) search over the IT knowledge base.

        Args:
            query: Natural language search query.
            user_role: Used to apply RBAC filter (employee → public only; it_admin → all).
            top_k: Maximum number of chunks to return.
            doc_versions: Optional list of doc_version values to restrict results
                          (e.g. ["v1_2025", "v1_2026"] for cross-version comparison).
        """
        ...
