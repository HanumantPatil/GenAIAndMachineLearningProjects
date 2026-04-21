"""Tests for AnswerKBQueryUseCase."""
import pytest
from tests.conftest import FakeKBSearchService, FakeLLMService
from src.application.use_cases.answer_kb_query_use_case import AnswerKBQueryUseCase
from src.domain.entities.kb_chunk import KBChunk
from src.domain.value_objects.user_role import UserRole


@pytest.fixture
def chunk():
    return KBChunk(
        chunk_id="c1", content="VPN steps here", source_file="vpn.pdf",
        doc_version="v1", page_number=2, access_role="public", score=0.9
    )


def test_returns_response_with_sources(chunk):
    kb = FakeKBSearchService(chunks=[chunk])
    llm = FakeLLMService(responses=["Connect to VPN via GlobalProtect."])
    uc = AnswerKBQueryUseCase(kb, llm)
    result = uc.execute("s1", "How do I connect to VPN?", UserRole.EMPLOYEE)
    assert "VPN" in result.response or result.response
    assert len(result.sources) == 1
    assert result.sources[0]["source_file"] == "vpn.pdf"


def test_confidence_score_is_average_of_chunks():
    chunks = [
        KBChunk("c1", "a", "f.pdf", "v1", 1, "public", score=0.8),
        KBChunk("c2", "b", "f.pdf", "v1", 2, "public", score=0.6),
    ]
    kb = FakeKBSearchService(chunks=chunks)
    llm = FakeLLMService(responses=["answer"])
    uc = AnswerKBQueryUseCase(kb, llm)
    result = uc.execute("s1", "query", UserRole.EMPLOYEE)
    assert result.confidence_score == pytest.approx(0.7)


def test_empty_chunks_returns_no_results_response():
    kb = FakeKBSearchService(chunks=[])
    llm = FakeLLMService(responses=["No information found."])
    uc = AnswerKBQueryUseCase(kb, llm)
    result = uc.execute("s1", "unknown", UserRole.EMPLOYEE)
    assert result.sources == []
    assert result.confidence_score == 0.0


def test_doc_versions_passed_to_search():
    recorded = []
    class RecordingKB(FakeKBSearchService):
        def search(self, query, user_role, top_k=5, doc_versions=None):
            recorded.append(doc_versions)
            return []
    kb = RecordingKB()
    llm = FakeLLMService(responses=["resp"])
    uc = AnswerKBQueryUseCase(kb, llm)
    uc.execute("s1", "q", UserRole.IT_ADMIN, doc_versions=["v1", "v2"])
    assert recorded[0] == ["v1", "v2"]
