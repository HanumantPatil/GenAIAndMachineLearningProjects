"""Tests for CosmosTicketRepository (mocked SDK)."""
import pytest
from unittest.mock import MagicMock, patch
from src.adapters.repositories.cosmos_ticket_repository import CosmosTicketRepository
from src.domain.entities.ticket import Ticket
from src.domain.value_objects.ticket_status import TicketStatus


@pytest.fixture
def mock_container():
    return MagicMock()


@pytest.fixture
def repo(mock_container):
    with patch("src.adapters.repositories.cosmos_ticket_repository.CosmosClient") as MockClient:
        MockClient.return_value.get_database_client.return_value.get_container_client.return_value = mock_container
        return CosmosTicketRepository("https://x", "key", "db", "Tickets"), mock_container


def test_create_calls_cosmos(repo):
    r, container = repo
    ticket = Ticket(id="TKT-1", user_id="u1", title="T", description="D")
    result = r.create(ticket)
    container.create_item.assert_called_once()
    assert result.id == "TKT-1"


def test_get_by_id_found(repo):
    r, container = repo
    ticket = Ticket(id="TKT-1", user_id="u1", title="T", description="D")
    container.read_item.return_value = ticket.to_dict()
    result = r.get_by_id("TKT-1", "u1")
    assert result.id == "TKT-1"


def test_get_by_id_not_found(repo):
    from azure.cosmos import exceptions as cosmos_exc
    r, container = repo
    container.read_item.side_effect = cosmos_exc.CosmosResourceNotFoundError(message="not found", response=MagicMock(status_code=404))
    result = r.get_by_id("TKT-NOPE", "u1")
    assert result is None


def test_get_latest_returns_ticket(repo):
    r, container = repo
    ticket = Ticket(id="TKT-1", user_id="u1", title="T", description="D")
    container.query_items.return_value = [ticket.to_dict()]
    result = r.get_latest("u1")
    assert result.id == "TKT-1"


def test_get_latest_empty(repo):
    r, container = repo
    container.query_items.return_value = []
    result = r.get_latest("u1")
    assert result is None


def test_update_calls_replace(repo):
    r, container = repo
    ticket = Ticket(id="TKT-1", user_id="u1", title="T", description="D")
    result = r.update(ticket)
    container.replace_item.assert_called_once()
    assert result.id == "TKT-1"


def test_list_by_user(repo):
    r, container = repo
    ticket = Ticket(id="TKT-1", user_id="u1", title="T", description="D")
    container.query_items.return_value = [ticket.to_dict()]
    results = r.list_by_user("u1")
    assert len(results) == 1
