"""KBChunk entity — a retrieved knowledge base document chunk."""
from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class KBChunk:
    chunk_id: str
    content: str
    source_file: str
    doc_version: str
    page_number: int
    access_role: str  # "public" | "it_admin"
    score: float = 0.0
    content_vector: list[float] = field(default_factory=list)

    def to_source_citation(self) -> dict:
        """Return a concise citation dict for API responses."""
        return {
            "source_file": self.source_file,
            "doc_version": self.doc_version,
            "page_number": self.page_number,
            "score": round(self.score, 4),
        }
