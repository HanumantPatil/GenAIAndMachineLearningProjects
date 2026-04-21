"""End-to-end orchestration test using all in-memory fakes — no Azure required."""
import json
import pytest
from tests.conftest import (
    FakeEscalationRepository, FakeKBSearchService, FakeLLMService,
    FakeNotificationService, FakeSessionRepository, FakeTicketRepository,
)
from src.application.dto.chat_request_dto import ChatRequestDTO
from src.application.use_cases.process_chat_use_case import ProcessChatUseCase
from src.domain.entities.kb_chunk import KBChunk
from src.domain.value_objects.user_role import UserRole


def _build_uc(llm_responses, kb_chunks=None):
    return ProcessChatUseCase(
        ticket_repo=FakeTicketRepository(),
        session_repo=FakeSessionRepository(),
        escalation_repo=FakeEscalationRepository(),
        kb_search=FakeKBSearchService(chunks=kb_chunks or []),
        llm=FakeLLMService(responses=llm_responses),
        notification=FakeNotificationService(case_id="ESC-E2E-001"),
    )


def _dto(msg, role="employee"):
    return ChatRequestDTO(session_id="e2e-s1", user_id="e2e-u1", user_role=UserRole(role), message=msg)


def test_e2e_kb_query_with_source():
    chunk = KBChunk("c1", "VPN: use GlobalProtect", "vpn.pdf", "v1", 1, "public", 0.92)
    llm_responses = [
        json.dumps({"intent": "kb_lookup", "kb_query": "VPN setup", "sub_intents": [], "ticket_id": None, "doc_versions": None}),
        "Use GlobalProtect to connect.",
    ]
    uc = _build_uc(llm_responses, kb_chunks=[chunk])
    result = uc.execute(_dto("How do I use VPN?"))
    assert result.response == "Use GlobalProtect to connect."
    assert result.sources[0]["source_file"] == "vpn.pdf"
    assert result.confidence_score >= 0.6


def test_e2e_ticket_create_and_status():
    llm_responses = [
        json.dumps({"intent": "ticket_create", "kb_query": None, "sub_intents": [], "ticket_id": None, "doc_versions": None}),
        json.dumps({"intent": "ticket_status", "kb_query": None, "sub_intents": [], "ticket_id": None, "doc_versions": None}),
    ]
    uc = _build_uc(llm_responses)
    r1 = uc.execute(_dto("My screen is broken"))
    assert r1.ticket_id is not None
    r2 = uc.execute(_dto("What is my ticket status?"))
    assert r2.ticket_id == r1.ticket_id


def test_e2e_auto_escalation_on_low_confidence():
    low_chunk = KBChunk("c1", "generic", "g.pdf", "v1", 1, "public", 0.1)
    llm_responses = [
        json.dumps({"intent": "kb_lookup", "kb_query": "arcane query", "sub_intents": [], "ticket_id": None, "doc_versions": None}),
        "weak answer",
        "Escalation summary.",
    ]
    uc = _build_uc(llm_responses, kb_chunks=[low_chunk])
    result = uc.execute(_dto("extremely obscure question"))
    assert result.escalation_case == "ESC-E2E-001"


def test_e2e_session_history_grows():
    llm_resp = [
        json.dumps({"intent": "unknown", "kb_query": None, "sub_intents": [], "ticket_id": None, "doc_versions": None}),
        json.dumps({"intent": "unknown", "kb_query": None, "sub_intents": [], "ticket_id": None, "doc_versions": None}),
    ]
    uc = _build_uc(llm_resp)
    uc.execute(_dto("first"))
    uc.execute(_dto("second"))
    session = uc._session_repo.get_history("e2e-s1")
    assert len(session.messages) == 4  # 2 turns × (user + assistant)
