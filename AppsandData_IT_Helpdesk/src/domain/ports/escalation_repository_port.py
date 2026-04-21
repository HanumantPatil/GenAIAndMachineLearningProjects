"""IEscalationRepository port — abstract interface for escalation case persistence."""
from abc import ABC, abstractmethod

from src.domain.entities.escalation_case import EscalationCase


class IEscalationRepository(ABC):
    @abstractmethod
    def create(self, case: EscalationCase) -> EscalationCase: ...

    @abstractmethod
    def get_by_id(self, case_id: str) -> EscalationCase | None: ...
