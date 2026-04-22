"""Tests for CosmosEscalationRepository (mocked SDK)."""
import datetime
from unittest.mock import MagicMock, patch
from azure.cosmos import exceptions as cosmos_exc
from src.adapters.repositories.cosmos_escalation_repository import CosmosEscalationRepository
from src.domain.entities.escalation_case import EscalationCase


def _make_repo():
    with patch("src.adapters.repositories.cosmos_escalation_repository.CosmosClient") as MockCosmos:
        container = MagicMock()
        MockCosmos.return_value.get_database_client.return_value.get_container_client.return_value = container
        repo = CosmosEscalationRepository("https://x", "key", "db", "escalations")
        return repo, container


def _sample_case():
    return EscalationCase(
        case_id="ESC-001",
        session_id="s1",
        user_id="u1",
        summary="VPN issue",
        created_at=datetime.datetime.now(datetime.timezone.utc),
    )


def test_create_calls_cosmos():
    repo, container = _make_repo()
    case = _sample_case()
    result = repo.create(case)
    container.create_item.assert_called_once()
    assert result is case


def test_get_by_id_found():
    repo, container = _make_repo()
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    container.read_item.return_value = {
        "caseId": "ESC-001", "sessionId": "s1", "userId": "u1",
        "summary": "VPN issue", "created_at": now, "notified": False,
    }
    result = repo.get_by_id("ESC-001")
    assert result is not None
    assert result.case_id == "ESC-001"


def test_get_by_id_not_found():
    repo, container = _make_repo()
    container.read_item.side_effect = cosmos_exc.CosmosResourceNotFoundError(
        message="nf", response=MagicMock(status_code=404)
    )
    result = repo.get_by_id("MISSING")
    assert result is None
