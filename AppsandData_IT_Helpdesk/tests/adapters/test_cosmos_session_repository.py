"""Tests for CosmosSessionRepository (mocked SDK)."""
import pytest
from unittest.mock import MagicMock, patch
from src.adapters.repositories.cosmos_session_repository import CosmosSessionRepository
from src.domain.entities.session import Session


@pytest.fixture
def mock_container():
    return MagicMock()


@pytest.fixture
def repo(mock_container):
    with patch("src.adapters.repositories.cosmos_session_repository.CosmosClient") as MC:
        MC.return_value.get_database_client.return_value.get_container_client.return_value = mock_container
        return CosmosSessionRepository("https://x", "key", "db", "Sessions"), mock_container


def test_get_or_create_creates_new(repo):
    r, container = repo
    from azure.cosmos import exceptions as cosmos_exc
    container.read_item.side_effect = cosmos_exc.CosmosResourceNotFoundError(message="nf", response=MagicMock(status_code=404))
    session = r.get_or_create("s1", "u1")
    container.create_item.assert_called_once()
    assert session.session_id == "s1"


def test_get_or_create_returns_existing(repo):
    r, container = repo
    s = Session(session_id="s1", user_id="u1")
    container.read_item.return_value = s.to_dict()
    session = r.get_or_create("s1", "u1")
    assert session.session_id == "s1"


def test_save_upserts(repo):
    r, container = repo
    s = Session(session_id="s1", user_id="u1")
    r.save(s)
    container.upsert_item.assert_called_once()


def test_get_history_found(repo):
    r, container = repo
    s = Session(session_id="s1", user_id="u1")
    container.read_item.return_value = s.to_dict()
    result = r.get_history("s1")
    assert result.session_id == "s1"


def test_get_history_not_found(repo):
    from azure.cosmos import exceptions as cosmos_exc
    r, container = repo
    container.read_item.side_effect = cosmos_exc.CosmosResourceNotFoundError(message="nf", response=MagicMock(status_code=404))
    result = r.get_history("s1")
    assert result is None
