"""Pydantic schemas for the FastAPI API layer."""
from __future__ import annotations
from typing import Any
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    session_id: str = Field(..., description="Unique session identifier.")
    user_id: str = Field(..., description="ID of the requesting user.")
    user_role: str = Field(default="employee", description="'employee' or 'it_admin'.")
    message: str = Field(..., min_length=1, max_length=4096, description="User message.")


class ChatResponse(BaseModel):
    session_id: str
    response: str
    sources: list[dict[str, Any]] = []
    ticket_id: str | None = None
    escalation_case: str | None = None
    confidence_score: float | None = None


class TicketResponse(BaseModel):
    ticket_id: str
    user_id: str
    title: str
    description: str
    status: str
    created_at: str
    updated_at: str
    resolution_notes: str | None = None


class HealthResponse(BaseModel):
    status: str = "ok"
    version: str = "1.0.0"
