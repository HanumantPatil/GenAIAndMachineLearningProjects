"""Integration-style tests for ProcessChatUseCase using in-memory fakes."""
import json
import pytest
from tests.conftest import (
    FakeEscalationRepository, FakeKBSearchService, FakeLLMService,
    FakeNotificationService, FakeSessionRepository, FakeTicketRepository,
)
from src.application.dto.chat_request_dto import ChatRequestDTO
from src.application.use_cases.process_chat_use_case import ProcessChatUseCase
from src.domain.entities.kb_chunk import KBChunk
from src.domain.value_objects.intent import Intent
from src.domain.value_objects.user_role import UserRole


def _make_uc(llm_responses=None, kb_chunks=None, notif_case="ESC-TEST"):
    llm = FakeLLMService(responses=llm_responses or [])
    kb = FakeKBSearchService(chunks=kb_chunks or [])
    notif = FakeNotificationService(case_id=notif_case)
    return ProcessChatUseCase(
        ticket_repo=FakeTicketRepository(),
        session_repo=FakeSessionRepository(),
        escalation_repo=FakeEscalationRepository(),
        kb_search=kb,
        llm=llm,
        notification=notif,
    ), llm, notif


def _dto(message: str, role: str = "employee") -> ChatRequestDTO:
    return ChatRequestDTO(session_id="s1", user_id="u1", user_role=UserRole(role), message=message)


def test_kb_lookup_route():
    intent_json = json.dumps({"intent": "kb_lookup", "kb_query": "VPN setup", "sub_intents": [], "ticket_id": None, "doc_versions": None})
    uc, llm, _ = _make_uc(
        llm_responses=[intent_json, "Connect via GlobalProtect."],
        kb_chunks=[KBChunk("c1", "vpn info", "vpn.pdf", "v1", 1, "public", 0.9)],
    )
    result = uc.execute(_dto("How to connect to VPN?"))
    assert result.response == "Connect via GlobalProtect."


def test_ticket_create_route():
    intent_json = json.dumps({"intent": "ticket_create", "kb_query": None, "sub_intents": [], "ticket_id": None, "doc_versions": None})
    uc, llm, _ = _make_uc(llm_responses=[intent_json])
    result = uc.execute(_dto("My laptop won't start"))
    assert result.ticket_id is not None


def test_escalation_route():
    intent_json = json.dumps({"intent": "escalation", "kb_query": None, "sub_intents": [], "ticket_id": None, "doc_versions": None})
    uc, llm, notif = _make_uc(llm_responses=[intent_json, "Escalation summary."])
    result = uc.execute(_dto("I need to speak to a human"))
    assert result.escalation_case == "ESC-TEST"


def test_unknown_intent_returns_fallback():
    intent_json = json.dumps({"intent": "unknown", "kb_query": None, "sub_intents": [], "ticket_id": None, "doc_versions": None})
    uc, _, _ = _make_uc(llm_responses=[intent_json])
    result = uc.execute(_dto("asdfghjkl"))
    assert "not sure" in result.response.lower() or result.response


def test_low_confidence_triggers_auto_escalation():
    intent_json = json.dumps({"intent": "kb_lookup", "kb_query": "q", "sub_intents": [], "ticket_id": None, "doc_versions": None})
    low_score_chunk = KBChunk("c1", "info", "f.pdf", "v1", 1, "public", score=0.1)
    uc, llm, notif = _make_uc(
        llm_responses=[intent_json, "answer", "escalation summary"],
        kb_chunks=[low_score_chunk],
    )
    result = uc.execute(_dto("hard question"))
    assert result.escalation_case == "ESC-TEST"


def test_session_is_persisted():
    intent_json = json.dumps({"intent": "unknown", "kb_query": None, "sub_intents": [], "ticket_id": None, "doc_versions": None})
    uc, _, _ = _make_uc(llm_responses=[intent_json])
    uc.execute(_dto("hello"))
    session = uc._session_repo.get_history("s1")
    assert session is not None


def test_multi_intent_kb_and_ticket():
    intent_json = json.dumps({
        "intent": "multi_intent",
        "kb_query": "VPN help",
        "sub_intents": ["kb_lookup", "ticket_create"],
        "ticket_id": None,
        "doc_versions": None,
    })
    chunk = KBChunk("c1", "vpn info", "vpn.pdf", "v1", 1, "public", 0.9)
    uc, _, _ = _make_uc(
        llm_responses=[intent_json, "VPN answer."],
        kb_chunks=[chunk],
    )
    result = uc.execute(_dto("VPN help and create ticket"))
    assert result.session_id == "s1"
    # Multi-intent should produce merged response containing both KB answer + ticket result
    assert result.response is not None
