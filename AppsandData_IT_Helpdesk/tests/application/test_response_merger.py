"""Tests for ResponseMerger."""
import pytest
from src.application.services.response_merger import ResponseMerger
from src.application.dto.chat_response_dto import ChatResponseDTO


def _resp(response: str, sources=None, confidence=None, ticket_id=None, escalation=None) -> ChatResponseDTO:
    return ChatResponseDTO(
        session_id="s1",
        response=response,
        sources=sources or [],
        confidence_score=confidence,
        ticket_id=ticket_id,
        escalation_case=escalation,
    )


def test_merge_combines_responses():
    r1 = _resp("Answer A")
    r2 = _resp("Answer B")
    merged = ResponseMerger.merge([r1, r2], "s1")
    assert "Answer A" in merged.response
    assert "Answer B" in merged.response


def test_merge_deduplicates_sources():
    src = {"source_file": "a.pdf", "page_number": 1}
    r1 = _resp("A", sources=[src])
    r2 = _resp("B", sources=[src])  # same (file, page)
    merged = ResponseMerger.merge([r1, r2], "s1")
    assert len(merged.sources) == 1


def test_merge_keeps_distinct_sources():
    r1 = _resp("A", sources=[{"source_file": "a.pdf", "page_number": 1}])
    r2 = _resp("B", sources=[{"source_file": "b.pdf", "page_number": 2}])
    merged = ResponseMerger.merge([r1, r2], "s1")
    assert len(merged.sources) == 2


def test_merge_takes_minimum_confidence():
    r1 = _resp("A", confidence=0.9)
    r2 = _resp("B", confidence=0.4)
    merged = ResponseMerger.merge([r1, r2], "s1")
    assert merged.confidence_score == pytest.approx(0.4)


def test_merge_no_confidence_is_none():
    r1 = _resp("A")
    r2 = _resp("B")
    merged = ResponseMerger.merge([r1, r2], "s1")
    assert merged.confidence_score is None


def test_merge_ticket_id_from_first_available():
    r1 = _resp("A", ticket_id="TKT-001")
    r2 = _resp("B")
    merged = ResponseMerger.merge([r1, r2], "s1")
    assert merged.ticket_id == "TKT-001"


def test_merge_escalation_from_first_available():
    r1 = _resp("A")
    r2 = _resp("B", escalation="ESC-001")
    merged = ResponseMerger.merge([r1, r2], "s1")
    assert merged.escalation_case == "ESC-001"


def test_merge_single_response_passthrough():
    r1 = _resp("Only response", confidence=0.75)
    merged = ResponseMerger.merge([r1], "s1")
    assert merged.response == "Only response"
    assert merged.confidence_score == 0.75


def test_merge_empty_list_returns_empty_response():
    merged = ResponseMerger.merge([], "s1")
    assert merged.session_id == "s1"
    assert merged.response == ""
    assert merged.sources == []
