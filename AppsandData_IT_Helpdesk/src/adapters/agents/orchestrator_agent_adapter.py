"""OrchestratorAgentAdapter — wires MAF OrchestratorAgent to ProcessChatUseCase."""
from __future__ import annotations

from src.application.dto.chat_request_dto import ChatRequestDTO
from src.application.use_cases.process_chat_use_case import ProcessChatUseCase
from src.domain.value_objects.user_role import UserRole


class OrchestratorAgentAdapter:
    """
    Entry point called by the FastAPI layer.
    Translates API request data → ChatRequestDTO → ProcessChatUseCase → response dict.

    In full MAF deployments this adapter would also register the agent with
    AIProjectClient and run a thread, but for the FastAPI-based deployment the
    use case is invoked directly (MAF agent instructions live in the system prompt).
    """

    def __init__(self, use_case: ProcessChatUseCase) -> None:
        self._use_case = use_case

    def chat(
        self,
        session_id: str,
        user_id: str,
        user_role: str,
        message: str,
    ) -> dict:
        try:
            role = UserRole(user_role)
        except ValueError:
            role = UserRole.EMPLOYEE

        dto = ChatRequestDTO(
            session_id=session_id,
            user_id=user_id,
            user_role=role,
            message=message,
        )
        result = self._use_case.execute(dto)
        return {
            "session_id": result.session_id,
            "response": result.response,
            "sources": result.sources,
            "ticket_id": result.ticket_id,
            "escalation_case": result.escalation_case,
            "confidence_score": result.confidence_score,
        }
