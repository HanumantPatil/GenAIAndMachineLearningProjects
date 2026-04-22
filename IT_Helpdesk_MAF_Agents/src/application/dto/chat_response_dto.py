"""ChatResponseDTO — output data transfer object from any use case."""
from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class ChatResponseDTO:
    session_id: str
    response: str
    sources: list[dict] = field(default_factory=list)
    ticket_id: str | None = None
    escalation_case: str | None = None
    confidence_score: float | None = None
