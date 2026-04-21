"""ManageTicketUseCase — create, read, and update support tickets."""
from __future__ import annotations
import uuid
from datetime import datetime, timezone

from src.application.dto.chat_response_dto import ChatResponseDTO
from src.domain.entities.ticket import Ticket
from src.domain.ports.ticket_repository_port import ITicketRepository
from src.domain.value_objects.intent import Intent
from src.domain.value_objects.ticket_status import TicketStatus


class ManageTicketUseCase:
    def __init__(self, ticket_repo: ITicketRepository) -> None:
        self._repo = ticket_repo

    def execute(
        self,
        session_id: str,
        intent: Intent,
        user_id: str,
        title: str = "",
        description: str = "",
        ticket_id: str | None = None,
        new_status: str | None = None,
        resolution_notes: str | None = None,
    ) -> ChatResponseDTO:
        if intent == Intent.TICKET_CREATE:
            return self._create_ticket(session_id, user_id, title, description)
        if intent == Intent.TICKET_STATUS:
            return self._get_ticket_status(session_id, user_id, ticket_id)
        if intent == Intent.TICKET_UPDATE:
            return self._update_ticket(
                session_id, user_id, ticket_id, new_status, resolution_notes
            )
        return ChatResponseDTO(
            session_id=session_id, response="Unknown ticket intent.", sources=[]
        )

    # ── Private helpers ──────────────────────────────────────────────────────

    def _create_ticket(
        self, session_id: str, user_id: str, title: str, description: str
    ) -> ChatResponseDTO:
        ticket = Ticket(
            id=f"TKT-{uuid.uuid4().hex[:8].upper()}",
            user_id=user_id,
            title=title or "Support Request",
            description=description or "No description provided.",
        )
        saved = self._repo.create(ticket)
        return ChatResponseDTO(
            session_id=session_id,
            response=(
                f"Ticket **{saved.id}** has been created successfully.\n"
                f"Title: {saved.title}\nStatus: {saved.status.value}"
            ),
            sources=[],
            ticket_id=saved.id,
        )

    def _get_ticket_status(
        self, session_id: str, user_id: str, ticket_id: str | None
    ) -> ChatResponseDTO:
        if ticket_id:
            ticket = self._repo.get_by_id(ticket_id, user_id)
        else:
            ticket = self._repo.get_latest(user_id)

        if not ticket:
            return ChatResponseDTO(
                session_id=session_id,
                response="No ticket found for your account.",
                sources=[],
            )
        return ChatResponseDTO(
            session_id=session_id,
            response=(
                f"Ticket **{ticket.id}**\n"
                f"Title: {ticket.title}\n"
                f"Status: {ticket.status.value}\n"
                f"Created: {ticket.created_at.strftime('%Y-%m-%d %H:%M UTC')}\n"
                f"Last updated: {ticket.updated_at.strftime('%Y-%m-%d %H:%M UTC')}"
            ),
            sources=[],
            ticket_id=ticket.id,
        )

    def _update_ticket(
        self,
        session_id: str,
        user_id: str,
        ticket_id: str | None,
        new_status: str | None,
        notes: str | None,
    ) -> ChatResponseDTO:
        if not ticket_id:
            return ChatResponseDTO(
                session_id=session_id,
                response="Please provide a ticket ID to update.",
                sources=[],
            )
        ticket = self._repo.get_by_id(ticket_id, user_id)
        if not ticket:
            return ChatResponseDTO(
                session_id=session_id,
                response=f"Ticket {ticket_id} not found.",
                sources=[],
            )
        if new_status:
            ticket.update_status(TicketStatus(new_status), notes)
            saved = self._repo.update(ticket)
            return ChatResponseDTO(
                session_id=session_id,
                response=f"Ticket **{saved.id}** updated to status: {saved.status.value}.",
                sources=[],
                ticket_id=saved.id,
            )
        return ChatResponseDTO(
            session_id=session_id,
            response="No changes to apply.",
            sources=[],
            ticket_id=ticket_id,
        )
