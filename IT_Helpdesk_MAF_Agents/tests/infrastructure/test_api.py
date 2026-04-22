"""FastAPI integration tests (no Azure connections required)."""
import json
import pytest
from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from src.infrastructure.api.main import app
from src.infrastructure.api.dependencies import get_process_chat_use_case
from src.application.dto.chat_response_dto import ChatResponseDTO


@pytest.fixture
def mock_use_case():
    uc = MagicMock()
    uc.execute.return_value = ChatResponseDTO(
        session_id="s1",
        response="Mocked answer.",
        sources=[],
        ticket_id=None,
        escalation_case=None,
        confidence_score=0.85,
    )
    uc._session_repo.get_history.return_value = None
    uc._ticket_use_case._repo.list_by_user.return_value = []
    return uc


@pytest.fixture
def client(mock_use_case):
    app.dependency_overrides[get_process_chat_use_case] = lambda: mock_use_case
    yield TestClient(app)
    app.dependency_overrides.clear()


def test_health_endpoint(client):
    resp = client.get("/api/v1/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_chat_endpoint_success(client):
    payload = {"session_id": "s1", "user_id": "u1", "user_role": "employee", "message": "How to reset VPN?"}
    resp = client.post("/api/v1/chat", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["response"] == "Mocked answer."
    assert data["confidence_score"] == 0.85


def test_chat_endpoint_missing_message(client):
    resp = client.post("/api/v1/chat", json={"session_id": "s1", "user_id": "u1"})
    assert resp.status_code == 422


def test_chat_endpoint_empty_message(client):
    resp = client.post("/api/v1/chat", json={"session_id": "s1", "user_id": "u1", "message": ""})
    assert resp.status_code == 422


def test_session_history_not_found(client):
    resp = client.get("/api/v1/sessions/nonexistent/history")
    assert resp.status_code == 404


def test_list_tickets_empty(client):
    resp = client.get("/api/v1/tickets/u1")
    assert resp.status_code == 200
    assert resp.json()["tickets"] == []


def test_chat_endpoint_invalid_user_role_defaults_to_employee(client):
    """Invalid user_role should fall back to employee without error."""
    payload = {"session_id": "s1", "user_id": "u1", "user_role": "superadmin", "message": "help"}
    resp = client.post("/api/v1/chat", json=payload)
    assert resp.status_code == 200


def test_session_history_found(client, mock_use_case):
    from src.domain.entities.session import Session
    session = Session(session_id="abc", user_id="u1")
    session.append_message("user", "hello")
    mock_use_case._session_repo.get_history.return_value = session
    resp = client.get("/api/v1/sessions/abc/history")
    assert resp.status_code == 200
    data = resp.json()
    assert data["session_id"] == "abc"
    assert len(data["messages"]) == 1


def test_chat_endpoint_invalid_user_role_defaults_to_employee(client):
    """Invalid user_role should fall back to employee without error."""
    payload = {"session_id": "s1", "user_id": "u1", "user_role": "superadmin", "message": "help"}
    resp = client.post("/api/v1/chat", json=payload)
    assert resp.status_code == 200


def test_session_history_found(client, mock_use_case):
    from src.domain.entities.session import Session
    session = Session(session_id="abc", user_id="u1")
    session.append_message("user", "hello")
    mock_use_case._session_repo.get_history.return_value = session
    resp = client.get("/api/v1/sessions/abc/history")
    assert resp.status_code == 200
    data = resp.json()
    assert data["session_id"] == "abc"
    assert len(data["messages"]) == 1


def test_unhandled_exception_returns_500(mock_use_case):
    """Use raise_server_exceptions=False so TestClient returns 500 instead of re-raising."""
    mock_use_case.execute.side_effect = RuntimeError("unexpected")
    app.dependency_overrides[get_process_chat_use_case] = lambda: mock_use_case
    try:
        error_client = TestClient(app, raise_server_exceptions=False)
        payload = {"session_id": "s1", "user_id": "u1", "message": "test"}
        resp = error_client.post("/api/v1/chat", json=payload)
        assert resp.status_code == 500
    finally:
        app.dependency_overrides.clear()
