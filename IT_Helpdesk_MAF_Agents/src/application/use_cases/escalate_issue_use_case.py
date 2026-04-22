"""EscalateIssueUseCase — compose an escalation summary, notify IT, and persist the case."""
from __future__ import annotations
import uuid
from datetime import datetime, timezone

from src.application.dto.chat_response_dto import ChatResponseDTO
from src.domain.entities.escalation_case import EscalationCase
from src.domain.ports.escalation_repository_port import IEscalationRepository
from src.domain.ports.llm_port import ILLMService
from src.domain.ports.notification_port import INotificationService

_ESCALATION_SYSTEM_PROMPT = """You are an IT escalation specialist.
Given the conversation history, write a concise, professional escalation summary (3-5 sentences)
that includes: the user's issue, steps already tried, and reason for escalation.
Do NOT include pleasantries or padding. Be factual and structured."""


class EscalateIssueUseCase:
    def __init__(
        self,
        llm: ILLMService,
        notification: INotificationService,
        escalation_repo: IEscalationRepository,
    ) -> None:
        self._llm = llm
        self._notification = notification
        self._escalation_repo = escalation_repo

    def execute(
        self,
        session_id: str,
        user_id: str,
        conversation_history: list[dict],
    ) -> ChatResponseDTO:
        # 1. Compose escalation summary via LLM
        messages = [
            {"role": "system", "content": _ESCALATION_SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"Conversation history:\n{self._format_history(conversation_history)}",
            },
        ]
        summary = self._llm.complete(messages)

        # 2. Notify IT support (simulated)
        case_id = self._notification.notify(user_id, summary)

        # 3. Persist escalation case
        case = EscalationCase(
            case_id=case_id,
            user_id=user_id,
            session_id=session_id,
            summary=summary,
        )
        case.mark_notified()
        self._escalation_repo.create(case)

        return ChatResponseDTO(
            session_id=session_id,
            response=(
                f"Your issue has been escalated to our IT support team.\n"
                f"**Escalation case reference:** {case_id}\n"
                f"A specialist will contact you shortly."
            ),
            sources=[],
            escalation_case=case_id,
        )

    @staticmethod
    def _format_history(history: list[dict]) -> str:
        return "\n".join(
            f"{turn.get('role', 'user').upper()}: {turn.get('content', '')}"
            for turn in history
        )
