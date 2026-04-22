"""ChatRequestDTO — input data transfer object for the /chat endpoint."""
from __future__ import annotations
from dataclasses import dataclass

from src.domain.value_objects.user_role import UserRole


@dataclass
class ChatRequestDTO:
    session_id: str
    user_id: str
    user_role: UserRole
    message: str
