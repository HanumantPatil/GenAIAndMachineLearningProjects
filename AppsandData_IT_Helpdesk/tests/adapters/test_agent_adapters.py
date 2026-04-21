"""Tests for agent adapters."""
import json
import pytest
from unittest.mock import MagicMock, patch
from src.adapters.agents.orchestrator_agent_adapter import OrchestratorAgentAdapter


# ── OrchestratorAgentAdapter ─────────────────────────────────────────────────

def test_orchestrator_chat_returns_dict():
    use_case = MagicMock()
    use_case.execute.return_value = MagicMock(
        session_id="s1", response="answer", sources=[], ticket_id=None,
        escalation_case=None, confidence_score=0.9
    )
    adapter = OrchestratorAgentAdapter(use_case)
    result = adapter.chat("s1", "u1", "employee", "hello")
    assert result["response"] == "answer"
    assert result["session_id"] == "s1"


def test_orchestrator_invalid_role_defaults_to_employee():
    use_case = MagicMock()
    use_case.execute.return_value = MagicMock(
        session_id="s1", response="hi", sources=[], ticket_id=None,
        escalation_case=None, confidence_score=None
    )
    adapter = OrchestratorAgentAdapter(use_case)
    result = adapter.chat("s1", "u1", "invalid_role", "hi")
    assert result["response"] == "hi"


# ── EmailNotificationService ─────────────────────────────────────────────────

def test_email_notification_returns_case_id():
    from src.adapters.services.email_notification_service import EmailNotificationService
    svc = EmailNotificationService("test@company.com")
    case_id = svc.notify("u1", "User cannot connect to VPN.")
    assert case_id.startswith("ESC-")


def test_email_notification_format():
    from src.adapters.services.email_notification_service import EmailNotificationService
    import re
    svc = EmailNotificationService("it@company.com")
    case_id = svc.notify("u2", "summary")
    assert re.match(r"ESC-\d{8}-[A-F0-9]{6}", case_id)
