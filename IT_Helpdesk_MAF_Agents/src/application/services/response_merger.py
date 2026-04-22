"""ResponseMerger — merges parallel ChatResponseDTOs into a single response."""
from __future__ import annotations

from src.application.dto.chat_response_dto import ChatResponseDTO


class ResponseMerger:
    @staticmethod
    def merge(responses: list[ChatResponseDTO], session_id: str) -> ChatResponseDTO:
        """
        Merge results from parallel use-case calls (multi_intent).

        Rules:
        - Response texts are joined with a double newline separator.
        - Sources lists are concatenated (deduplicated by source_file+page).
        - ticket_id is taken from whichever response has one.
        - escalation_case is taken from whichever response has one.
        - confidence_score is the minimum across all responses (most conservative).
        """
        if not responses:
            return ChatResponseDTO(session_id=session_id, response="", sources=[])

        if len(responses) == 1:
            return responses[0]

        combined_response = "\n\n".join(r.response for r in responses if r.response)

        # Deduplicate sources by (source_file, page_number) key
        seen: set[tuple] = set()
        combined_sources: list[dict] = []
        for r in responses:
            for s in r.sources:
                key = (s.get("source_file"), s.get("page_number"))
                if key not in seen:
                    seen.add(key)
                    combined_sources.append(s)

        ticket_id = next((r.ticket_id for r in responses if r.ticket_id), None)
        escalation_case = next((r.escalation_case for r in responses if r.escalation_case), None)
        scores = [r.confidence_score for r in responses if r.confidence_score is not None]
        confidence = min(scores) if scores else None

        return ChatResponseDTO(
            session_id=session_id,
            response=combined_response,
            sources=combined_sources,
            ticket_id=ticket_id,
            escalation_case=escalation_case,
            confidence_score=confidence,
        )
