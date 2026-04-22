"""INotificationService port — abstract interface for escalation notifications."""
from abc import ABC, abstractmethod


class INotificationService(ABC):
    @abstractmethod
    def notify(self, user_id: str, summary: str) -> str:
        """
        Send an escalation notification to IT support.

        Args:
            user_id: The employee whose issue is being escalated.
            summary: Structured escalation summary text.

        Returns:
            A unique case reference ID (e.g., "ESC-20260421-abc123").
        """
        ...
