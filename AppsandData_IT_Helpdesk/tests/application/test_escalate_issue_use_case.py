"""Tests for EscalateIssueUseCase."""
import pytest
from tests.conftest import FakeEscalationRepository, FakeLLMService, FakeNotificationService
from src.application.use_cases.escalate_issue_use_case import EscalateIssueUseCase


@pytest.fixture
def uc(fake_llm, fake_notification, fake_escalation_repo):
    fake_llm._responses = ["User cannot connect to VPN after multiple attempts."]
    return EscalateIssueUseCase(fake_llm, fake_notification, fake_escalation_repo)


def test_returns_case_id(uc, fake_escalation_repo):
    result = uc.execute("s1", "u1", [{"role": "user", "content": "Need help"}])
    assert result.escalation_case == "ESC-20240101-ABCDEF"


def test_persists_escalation_case(uc, fake_escalation_repo):
    uc.execute("s1", "u1", [{"role": "user", "content": "Help"}])
    assert "ESC-20240101-ABCDEF" in fake_escalation_repo._store


def test_notifies_it_support(uc, fake_notification):
    uc.execute("s1", "u1", [{"role": "user", "content": "Help"}])
    assert len(fake_notification.notified) == 1
    assert fake_notification.notified[0][0] == "u1"


def test_response_contains_case_reference(uc):
    result = uc.execute("s1", "u1", [])
    assert "ESC-20240101-ABCDEF" in result.response


def test_escalation_case_is_marked_notified(uc, fake_escalation_repo):
    uc.execute("s1", "u1", [])
    case = fake_escalation_repo._store["ESC-20240101-ABCDEF"]
    assert case.notified is True


def test_format_history_empty():
    from src.application.use_cases.escalate_issue_use_case import EscalateIssueUseCase
    result = EscalateIssueUseCase._format_history([])
    assert result == ""


def test_format_history_with_turns():
    turns = [{"role": "user", "content": "hi"}, {"role": "assistant", "content": "hello"}]
    result = EscalateIssueUseCase._format_history(turns)
    assert "USER: hi" in result
    assert "ASSISTANT: hello" in result
