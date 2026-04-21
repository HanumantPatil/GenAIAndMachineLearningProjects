"""API router for /api/v1 endpoints."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from src.application.use_cases.process_chat_use_case import ProcessChatUseCase
from src.application.dto.chat_request_dto import ChatRequestDTO
from src.domain.ports.ticket_repository_port import ITicketRepository
from src.domain.value_objects.user_role import UserRole
from src.infrastructure.api.dependencies import get_process_chat_use_case
from src.infrastructure.api.models.schemas import (
    ChatRequest,
    ChatResponse,
    HealthResponse,
    TicketResponse,
)

router = APIRouter(prefix="/api/v1", tags=["helpdesk"])


@router.post("/chat", response_model=ChatResponse)
def chat(
    body: ChatRequest,
    use_case: ProcessChatUseCase = Depends(get_process_chat_use_case),
) -> ChatResponse:
    try:
        role = UserRole(body.user_role)
    except ValueError:
        role = UserRole.EMPLOYEE

    dto = ChatRequestDTO(
        session_id=body.session_id,
        user_id=body.user_id,
        user_role=role,
        message=body.message,
    )
    result = use_case.execute(dto)
    return ChatResponse(
        session_id=result.session_id,
        response=result.response,
        sources=result.sources,
        ticket_id=result.ticket_id,
        escalation_case=result.escalation_case,
        confidence_score=result.confidence_score,
    )


@router.get("/sessions/{session_id}/history")
def get_session_history(
    session_id: str,
    use_case: ProcessChatUseCase = Depends(get_process_chat_use_case),
) -> dict:
    session = use_case._session_repo.get_history(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found.")
    return {"session_id": session_id, "messages": [m.to_dict() for m in session.messages]}


@router.get("/tickets/{user_id}")
def list_tickets(
    user_id: str,
    use_case: ProcessChatUseCase = Depends(get_process_chat_use_case),
) -> dict:
    tickets = use_case._ticket_use_case._repo.list_by_user(user_id)
    return {"user_id": user_id, "tickets": [t.to_dict() for t in tickets]}


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse()
