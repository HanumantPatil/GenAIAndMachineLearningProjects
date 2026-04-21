"""Session entity — conversation history container with TTL support."""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone

from src.domain.entities.message import Message

DEFAULT_TTL_SECONDS = 86400  # 24 hours


@dataclass
class Session:
    session_id: str
    user_id: str
    messages: list[Message] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    ttl: int = DEFAULT_TTL_SECONDS

    def append_message(self, role: str, content: str) -> Message:
        msg = Message(role=role, content=content)
        self.messages.append(msg)
        return msg

    def get_history(self, last_n: int | None = None) -> list[Message]:
        """Return last N messages (or all if last_n is None)."""
        if last_n is None:
            return list(self.messages)
        return list(self.messages[-last_n:])

    def to_dict(self) -> dict:
        return {
            "id": self.session_id,
            "sessionId": self.session_id,
            "userId": self.user_id,
            "messages": [m.to_dict() for m in self.messages],
            "created_at": self.created_at.isoformat(),
            "ttl": self.ttl,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Session":
        return cls(
            session_id=data["sessionId"],
            user_id=data["userId"],
            messages=[Message.from_dict(m) for m in data.get("messages", [])],
            created_at=datetime.fromisoformat(data["created_at"]),
            ttl=data.get("ttl", DEFAULT_TTL_SECONDS),
        )
