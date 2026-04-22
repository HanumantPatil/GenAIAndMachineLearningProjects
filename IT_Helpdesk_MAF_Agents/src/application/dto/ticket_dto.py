"""TicketDTO — data transfer object for ticket read/write operations."""
from __future__ import annotations
from dataclasses import dataclass

from src.domain.value_objects.ticket_status import TicketStatus


@dataclass
class TicketDTO:
    ticket_id: str
    user_id: str
    title: str
    description: str
    status: TicketStatus
    created_at: str
    updated_at: str
    resolution_notes: str | None = None
