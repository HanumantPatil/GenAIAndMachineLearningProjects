"""ISessionRepository port — abstract interface for session persistence."""
from abc import ABC, abstractmethod

from src.domain.entities.session import Session


class ISessionRepository(ABC):
    @abstractmethod
    def get_or_create(self, session_id: str, user_id: str) -> Session: ...

    @abstractmethod
    def save(self, session: Session) -> Session: ...

    @abstractmethod
    def get_history(self, session_id: str) -> Session | None: ...
