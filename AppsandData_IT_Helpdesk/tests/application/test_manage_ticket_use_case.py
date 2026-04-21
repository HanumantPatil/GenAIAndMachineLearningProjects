"""Tests for ManageTicketUseCase."""
import pytest
from tests.conftest import FakeTicketRepository
from src.application.use_cases.manage_ticket_use_case import ManageTicketUseCase
from src.domain.value_objects.intent import Intent
from src.domain.value_objects.ticket_status import TicketStatus


@pytest.fixture
def repo():
    return FakeTicketRepository()


@pytest.fixture
def uc(repo):
    return ManageTicketUseCase(repo)


def test_create_ticket(uc, repo):
    result = uc.execute("s1", Intent.TICKET_CREATE, "u1", title="Laptop issue", description="Won't boot")
    assert result.ticket_id is not None
    assert "created" in result.response.lower()
    assert len(repo._store) == 1


def test_create_ticket_default_title(uc):
    result = uc.execute("s1", Intent.TICKET_CREATE, "u1")
    assert result.ticket_id is not None


def test_get_ticket_status_by_id(uc, repo):
    created = uc.execute("s1", Intent.TICKET_CREATE, "u1", title="T", description="D")
    result = uc.execute("s1", Intent.TICKET_STATUS, "u1", ticket_id=created.ticket_id)
    assert result.ticket_id == created.ticket_id


def test_get_ticket_status_latest(uc):
    uc.execute("s1", Intent.TICKET_CREATE, "u1", title="T1", description="D1")
    result = uc.execute("s1", Intent.TICKET_STATUS, "u1")
    assert result.ticket_id is not None


def test_get_ticket_status_not_found(uc):
    result = uc.execute("s1", Intent.TICKET_STATUS, "u1")
    assert "no ticket" in result.response.lower()


def test_update_ticket_status(uc):
    created = uc.execute("s1", Intent.TICKET_CREATE, "u1", title="T", description="D")
    result = uc.execute(
        "s1", Intent.TICKET_UPDATE, "u1",
        ticket_id=created.ticket_id, new_status="in_progress"
    )
    assert "in_progress" in result.response.lower() or "in progress" in result.response.lower()


def test_update_ticket_no_ticket_id(uc):
    result = uc.execute("s1", Intent.TICKET_UPDATE, "u1", new_status="in_progress")
    assert "provide" in result.response.lower()


def test_update_ticket_not_found(uc):
    result = uc.execute("s1", Intent.TICKET_UPDATE, "u1", ticket_id="TKT-NOPE", new_status="in_progress")
    assert "not found" in result.response.lower()


def test_update_ticket_no_status(uc):
    created = uc.execute("s1", Intent.TICKET_CREATE, "u1", title="T", description="D")
    result = uc.execute("s1", Intent.TICKET_UPDATE, "u1", ticket_id=created.ticket_id)
    assert "no changes" in result.response.lower()


def test_unknown_intent_returns_fallback(uc):
    result = uc.execute("s1", Intent.UNKNOWN, "u1")
    assert "unknown" in result.response.lower()
