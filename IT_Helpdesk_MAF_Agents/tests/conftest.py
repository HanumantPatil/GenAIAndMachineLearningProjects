"""Shared in-memory fakes for all port interfaces used across the test suite."""
from __future__ import annotations
import pytest
from datetime import datetime, timezone
from src.domain.entities.escalation_case import EscalationCase
from src.domain.entities.session import Session
from src.domain.entities.ticket import Ticket
from src.domain.entities.kb_chunk import KBChunk
from src.domain.ports.escalation_repository_port import IEscalationRepository
from src.domain.ports.kb_search_port import IKBSearchService
from src.domain.ports.llm_port import ILLMService
from src.domain.ports.notification_port import INotificationService
from src.domain.ports.session_repository_port import ISessionRepository
from src.domain.ports.ticket_repository_port import ITicketRepository
from src.domain.value_objects.user_role import UserRole


# ── In-memory fakes ──────────────────────────────────────────────────────────

class FakeTicketRepository(ITicketRepository):
    def __init__(self):
        self._store: dict[str, Ticket] = {}

    def create(self, ticket: Ticket) -> Ticket:
        self._store[ticket.id] = ticket
        return ticket

    def get_by_id(self, ticket_id: str, user_id: str) -> Ticket | None:
        t = self._store.get(ticket_id)
        return t if t and t.user_id == user_id else None

    def get_latest(self, user_id: str) -> Ticket | None:
        user_tickets = [t for t in self._store.values() if t.user_id == user_id]
        return sorted(user_tickets, key=lambda t: t.created_at, reverse=True)[0] if user_tickets else None

    def update(self, ticket: Ticket) -> Ticket:
        self._store[ticket.id] = ticket
        return ticket

    def list_by_user(self, user_id: str) -> list[Ticket]:
        return [t for t in self._store.values() if t.user_id == user_id]


class FakeSessionRepository(ISessionRepository):
    def __init__(self):
        self._store: dict[str, Session] = {}

    def get_or_create(self, session_id: str, user_id: str) -> Session:
        if session_id not in self._store:
            self._store[session_id] = Session(session_id=session_id, user_id=user_id)
        return self._store[session_id]

    def save(self, session: Session) -> Session:
        self._store[session.session_id] = session
        return session

    def get_history(self, session_id: str) -> Session | None:
        return self._store.get(session_id)


class FakeEscalationRepository(IEscalationRepository):
    def __init__(self):
        self._store: dict[str, EscalationCase] = {}

    def create(self, case: EscalationCase) -> EscalationCase:
        self._store[case.case_id] = case
        return case

    def get_by_id(self, case_id: str) -> EscalationCase | None:
        return self._store.get(case_id)


class FakeKBSearchService(IKBSearchService):
    def __init__(self, chunks: list[KBChunk] | None = None):
        self._chunks = chunks or []

    def search(self, query: str, user_role: UserRole, top_k: int = 5, doc_versions=None) -> list[KBChunk]:
        return self._chunks[:top_k]


class FakeLLMService(ILLMService):
    def __init__(self, responses: list[str] | None = None):
        self._responses = list(responses or [])
        self._calls: list[list[dict]] = []

    def complete(self, messages: list[dict]) -> str:
        self._calls.append(messages)
        return self._responses.pop(0) if self._responses else "LLM default response."


class FakeNotificationService(INotificationService):
    def __init__(self, case_id: str = "ESC-20240101-ABCDEF"):
        self._case_id = case_id
        self.notified: list[tuple[str, str]] = []

    def notify(self, user_id: str, summary: str) -> str:
        self.notified.append((user_id, summary))
        return self._case_id


# ── pytest fixtures ──────────────────────────────────────────────────────────

@pytest.fixture
def fake_ticket_repo():
    return FakeTicketRepository()

@pytest.fixture
def fake_session_repo():
    return FakeSessionRepository()

@pytest.fixture
def fake_escalation_repo():
    return FakeEscalationRepository()

@pytest.fixture
def fake_kb_search():
    return FakeKBSearchService()

@pytest.fixture
def fake_llm():
    return FakeLLMService()

@pytest.fixture
def fake_notification():
    return FakeNotificationService()

@pytest.fixture
def sample_chunk():
    return KBChunk(
        chunk_id="c1",
        content="Reset your password at account.company.com/reset",
        source_file="password_policy.pdf",
        doc_version="v2.0",
        page_number=3,
        access_role="public",
        score=0.85,
    )
