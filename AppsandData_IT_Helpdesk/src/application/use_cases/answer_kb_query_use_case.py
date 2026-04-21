"""AnswerKBQueryUseCase — RAG: retrieve chunks, ground the answer, score confidence."""
from __future__ import annotations

from src.application.dto.chat_response_dto import ChatResponseDTO
from src.domain.ports.kb_search_port import IKBSearchService
from src.domain.ports.llm_port import ILLMService
from src.domain.value_objects.confidence_score import ConfidenceScore
from src.domain.value_objects.user_role import UserRole

_RAG_SYSTEM_PROMPT = """You are an IT support assistant. Answer the user's question ONLY using
the provided knowledge base excerpts. Always cite the source document.
If you cannot answer from the excerpts, say so clearly.
Always respond in English, regardless of the language of the source documents."""


class AnswerKBQueryUseCase:
    def __init__(self, kb_search: IKBSearchService, llm: ILLMService) -> None:
        self._kb_search = kb_search
        self._llm = llm

    def execute(
        self,
        session_id: str,
        query: str,
        user_role: UserRole,
        doc_versions: list[str] | None = None,
    ) -> ChatResponseDTO:
        chunks = self._kb_search.search(
            query=query,
            user_role=user_role,
            top_k=5,
            doc_versions=doc_versions,
        )

        if not chunks:
            return ChatResponseDTO(
                session_id=session_id,
                response="I could not find relevant information in the knowledge base.",
                sources=[],
                confidence_score=0.0,
            )

        context_parts = [
            f"[Source: {c.source_file} | Version: {c.doc_version} | Page: {c.page_number}]\n{c.content}"
            for c in chunks
        ]
        context = "\n\n---\n\n".join(context_parts)

        messages = [
            {"role": "system", "content": _RAG_SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"Knowledge base excerpts:\n\n{context}\n\nQuestion: {query}",
            },
        ]
        answer = self._llm.complete(messages)

        avg_score = sum(c.score for c in chunks) / len(chunks)
        confidence = ConfidenceScore(min(max(avg_score, 0.0), 1.0))

        return ChatResponseDTO(
            session_id=session_id,
            response=answer,
            sources=[c.to_source_citation() for c in chunks],
            confidence_score=confidence.value,
        )
