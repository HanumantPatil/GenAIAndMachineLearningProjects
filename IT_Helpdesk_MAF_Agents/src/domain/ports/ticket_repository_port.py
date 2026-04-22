"""ITicketRepository port — abstract interface for ticket persistence."""
from abc import ABC, abstractmethod

from src.domain.entities.ticket import Ticket


class ITicketRepository(ABC):
    @abstractmethod
    def create(self, ticket: Ticket) -> Ticket: ...

    @abstractmethod
    def get_by_id(self, ticket_id: str, user_id: str) -> Ticket | None: ...

    @abstractmethod
    def get_latest(self, user_id: str) -> Ticket | None: ...

    @abstractmethod
    def update(self, ticket: Ticket) -> Ticket: ...

    @abstractmethod
    def list_by_user(self, user_id: str) -> list[Ticket]: ...
