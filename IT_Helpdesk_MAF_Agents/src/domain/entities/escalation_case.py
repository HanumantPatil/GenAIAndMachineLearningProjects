"""EscalationCase entity — records a human-escalation event."""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class EscalationCase:
    case_id: str
    user_id: str
    session_id: str
    summary: str
    notified: bool = False
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def mark_notified(self) -> None:
        self.notified = True

    def to_dict(self) -> dict:
        return {
            "id": self.case_id,
            "caseId": self.case_id,
            "userId": self.user_id,
            "sessionId": self.session_id,
            "summary": self.summary,
            "notified": self.notified,
            "created_at": self.created_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "EscalationCase":
        return cls(
            case_id=data["caseId"],
            user_id=data["userId"],
            session_id=data["sessionId"],
            summary=data["summary"],
            notified=data.get("notified", False),
            created_at=datetime.fromisoformat(data["created_at"]),
        )
