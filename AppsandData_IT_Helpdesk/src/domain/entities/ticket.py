"""Ticket entity — core support ticket aggregate root."""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone

from src.domain.value_objects.ticket_status import TicketStatus


@dataclass
class Ticket:
    id: str
    user_id: str
    title: str
    description: str
    status: TicketStatus = TicketStatus.OPEN
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    resolution_notes: str | None = None

    def update_status(self, new_status: TicketStatus, notes: str | None = None) -> None:
        """Transition status with domain rule validation."""
        if not self.status.can_transition_to(new_status):
            raise ValueError(
                f"Cannot transition ticket from '{self.status}' to '{new_status}'"
            )
        self.status = new_status
        self.updated_at = datetime.now(timezone.utc)
        if notes:
            self.resolution_notes = notes

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "userId": self.user_id,
            "title": self.title,
            "description": self.description,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "resolution_notes": self.resolution_notes,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Ticket":
        return cls(
            id=data["id"],
            user_id=data["userId"],
            title=data["title"],
            description=data["description"],
            status=TicketStatus(data["status"]),
            created_at=datetime.fromisoformat(data["created_at"]),
            updated_at=datetime.fromisoformat(data["updated_at"]),
            resolution_notes=data.get("resolution_notes"),
        )
