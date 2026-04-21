"""Tests for all domain entities."""
import pytest
from datetime import datetime, timezone
from src.domain.entities.escalation_case import EscalationCase
from src.domain.entities.kb_chunk import KBChunk
from src.domain.entities.message import Message
from src.domain.entities.session import Session
from src.domain.entities.ticket import Ticket
from src.domain.value_objects.ticket_status import TicketStatus


class TestMessage:
    def test_to_dict_roundtrip(self):
        m = Message(role="user", content="hello")
        d = m.to_dict()
        m2 = Message.from_dict(d)
        assert m2.role == "user"
        assert m2.content == "hello"

    def test_timestamp_default_is_utc(self):
        m = Message(role="assistant", content="hi")
        assert m.timestamp.tzinfo is not None


class TestTicket:
    def test_default_status_is_open(self):
        t = Ticket(id="TKT-1", user_id="u1", title="Test", description="Desc")
        assert t.status == TicketStatus.OPEN

    def test_update_status_valid(self):
        t = Ticket(id="TKT-1", user_id="u1", title="T", description="D")
        t.update_status(TicketStatus.IN_PROGRESS)
        assert t.status == TicketStatus.IN_PROGRESS

    def test_update_status_invalid_raises(self):
        t = Ticket(id="TKT-1", user_id="u1", title="T", description="D")
        with pytest.raises(ValueError):
            t.update_status(TicketStatus.RESOLVED)

    def test_to_dict_uses_userId_key(self):
        t = Ticket(id="TKT-1", user_id="u1", title="T", description="D")
        d = t.to_dict()
        assert "userId" in d

    def test_from_dict_roundtrip(self):
        t = Ticket(id="TKT-1", user_id="u1", title="T", description="D")
        t2 = Ticket.from_dict(t.to_dict())
        assert t2.id == t.id
        assert t2.user_id == t.user_id
        assert t2.status == t.status

    def test_update_status_sets_notes(self):
        t = Ticket(id="TKT-1", user_id="u1", title="T", description="D")
        t.update_status(TicketStatus.IN_PROGRESS, "Working on it")
        t.update_status(TicketStatus.RESOLVED, "Fixed")
        assert t.resolution_notes == "Fixed"


class TestSession:
    def test_append_message_returns_message(self):
        s = Session(session_id="s1", user_id="u1")
        m = s.append_message("user", "hello")
        assert m.content == "hello"
        assert len(s.messages) == 1

    def test_get_history_last_n(self):
        s = Session(session_id="s1", user_id="u1")
        for i in range(10):
            s.append_message("user", f"msg {i}")
        history = s.get_history(last_n=3)
        assert len(history) == 3
        assert history[-1].content == "msg 9"

    def test_get_history_all_when_none(self):
        s = Session(session_id="s1", user_id="u1")
        for i in range(5):
            s.append_message("user", f"msg {i}")
        history = s.get_history()  # last_n=None → returns all
        assert len(history) == 5

    def test_to_dict_has_sessionId(self):
        s = Session(session_id="s1", user_id="u1")
        d = s.to_dict()
        assert d["sessionId"] == "s1"
        assert d["id"] == "s1"

    def test_from_dict_roundtrip(self):
        s = Session(session_id="s1", user_id="u1")
        s.append_message("user", "test")
        s2 = Session.from_dict(s.to_dict())
        assert s2.session_id == "s1"
        assert len(s2.messages) == 1


class TestKBChunk:
    def test_to_source_citation(self, sample_chunk):
        citation = sample_chunk.to_source_citation()
        assert citation["source_file"] == "password_policy.pdf"
        assert citation["page_number"] == 3
        assert citation["doc_version"] == "v2.0"
        assert citation["score"] == 0.85


class TestEscalationCase:
    def test_mark_notified(self):
        c = EscalationCase(case_id="ESC-1", user_id="u1", session_id="s1", summary="issue")
        assert c.notified is False
        c.mark_notified()
        assert c.notified is True

    def test_to_dict_uses_caseId(self):
        c = EscalationCase(case_id="ESC-1", user_id="u1", session_id="s1", summary="x")
        d = c.to_dict()
        assert "caseId" in d

    def test_from_dict_roundtrip(self):
        c = EscalationCase(case_id="ESC-1", user_id="u1", session_id="s1", summary="x")
        c2 = EscalationCase.from_dict(c.to_dict())
        assert c2.case_id == "ESC-1"
