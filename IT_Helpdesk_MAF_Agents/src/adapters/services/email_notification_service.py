"""EmailNotificationService — INotificationService (simulated email/Teams alert)."""
from __future__ import annotations
import uuid
import logging
from datetime import datetime, timezone

from src.domain.ports.notification_port import INotificationService

logger = logging.getLogger(__name__)


class EmailNotificationService(INotificationService):
    def __init__(self, escalation_email: str) -> None:
        self._email = escalation_email

    def notify(self, user_id: str, summary: str) -> str:
        """
        Simulates sending an email / Teams card to IT support.
        Returns a unique escalation case reference ID.
        """
        case_id = f"ESC-{datetime.now(timezone.utc).strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"
        logger.info(
            "ESCALATION NOTIFICATION\n"
            "  Case ID  : %s\n"
            "  User     : %s\n"
            "  To       : %s\n"
            "  Summary  : %s",
            case_id,
            user_id,
            self._email,
            summary,
        )
        return case_id
