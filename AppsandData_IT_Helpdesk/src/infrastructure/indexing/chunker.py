"""Document chunker — splits text into overlapping chunks for indexing."""
from __future__ import annotations
import re
import uuid


def chunk_text(
    text: str,
    source_file: str,
    doc_version: str,
    access_role: str = "public",
    chunk_size: int = 512,
    overlap: int = 64,
) -> list[dict]:
    """Split *text* into overlapping token-ish chunks and return index documents."""
    words = text.split()
    chunks: list[dict] = []
    start = 0
    page = 1

    while start < len(words):
        end = min(start + chunk_size, len(words))
        chunk_words = words[start:end]
        content = " ".join(chunk_words)

        chunks.append(
            {
                "id": uuid.uuid4().hex,
                "content": content,
                "source_file": source_file,
                "doc_version": doc_version,
                "page_number": page,
                "access_role": access_role,
            }
        )
        page += 1
        if end >= len(words):
            break
        start = end - overlap

    return chunks
