"""Intent value object — possible intents the orchestrator can classify."""
from enum import Enum


class Intent(str, Enum):
    KB_LOOKUP = "kb_lookup"
    TICKET_CREATE = "ticket_create"
    TICKET_STATUS = "ticket_status"
    TICKET_UPDATE = "ticket_update"
    ESCALATION = "escalation"
    MULTI_INTENT = "multi_intent"
    UNKNOWN = "unknown"
