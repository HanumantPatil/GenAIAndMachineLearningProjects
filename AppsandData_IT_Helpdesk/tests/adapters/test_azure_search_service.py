"""Tests for AzureSearchService (mocked SDK)."""
import pytest
from unittest.mock import MagicMock, patch
from src.adapters.services.azure_search_service import AzureSearchService
from src.domain.value_objects.user_role import UserRole


@pytest.fixture
def mock_search_client():
    return MagicMock()


@pytest.fixture
def svc(mock_search_client):
    with patch("src.adapters.services.azure_search_service.SearchClient") as MC:
        MC.return_value = mock_search_client
        return AzureSearchService("https://x", "key", "index"), mock_search_client


def _fake_result(content="info", source_file="doc.pdf", doc_version="v1", page_number=1, score=0.8):
    r = {
        "id": "c1", "content": content, "source_file": source_file,
        "doc_version": doc_version, "page_number": page_number,
        "access_role": "public", "@search.score": score,
    }
    return r


def test_search_employee_has_rbac_filter(svc):
    service, client = svc
    client.search.return_value = []
    service.search("vpn", UserRole.EMPLOYEE)
    call_kwargs = client.search.call_args[1]
    assert "public" in (call_kwargs.get("filter") or "")


def test_search_admin_no_filter(svc):
    service, client = svc
    client.search.return_value = []
    service.search("vpn", UserRole.IT_ADMIN)
    call_kwargs = client.search.call_args[1]
    assert call_kwargs.get("filter") is None


def test_search_returns_chunks(svc):
    service, client = svc
    client.search.return_value = [_fake_result()]
    chunks = service.search("vpn", UserRole.EMPLOYEE)
    assert len(chunks) == 1
    assert chunks[0].source_file == "doc.pdf"
    assert chunks[0].score == 0.8


def test_search_doc_versions_filter(svc):
    service, client = svc
    client.search.return_value = []
    service.search("vpn", UserRole.IT_ADMIN, doc_versions=["v1", "v2"])
    call_kwargs = client.search.call_args[1]
    assert "v1" in (call_kwargs.get("filter") or "")
    assert "v2" in (call_kwargs.get("filter") or "")


def test_search_with_embedding_fn(mock_search_client):
    with patch("src.adapters.services.azure_search_service.SearchClient") as MC:
        MC.return_value = mock_search_client
        mock_search_client.search.return_value = []
        embed_fn = lambda q: [0.1] * 3072
        svc = AzureSearchService("https://x", "key", "index", embedding_fn=embed_fn)
        svc.search("query", UserRole.EMPLOYEE)
        call_kwargs = mock_search_client.search.call_args[1]
        assert call_kwargs.get("vector_queries") is not None
