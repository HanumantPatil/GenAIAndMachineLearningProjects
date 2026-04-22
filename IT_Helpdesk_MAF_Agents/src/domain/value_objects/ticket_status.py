"""TicketStatus value object — valid lifecycle states for a support ticket."""
from enum import Enum


class TicketStatus(str, Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"

    def can_transition_to(self, target: "TicketStatus") -> bool:
        """Enforce valid ticket state transitions."""
        allowed: dict["TicketStatus", set["TicketStatus"]] = {
            TicketStatus.OPEN: {TicketStatus.IN_PROGRESS, TicketStatus.CLOSED},
            TicketStatus.IN_PROGRESS: {TicketStatus.RESOLVED, TicketStatus.CLOSED},
            TicketStatus.RESOLVED: {TicketStatus.CLOSED},
            TicketStatus.CLOSED: set(),
        }
        return target in allowed[self]
