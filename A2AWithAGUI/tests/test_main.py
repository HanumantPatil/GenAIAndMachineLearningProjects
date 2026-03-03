# Copyright (c) Microsoft. All rights reserved.

"""Unit tests for the FastAPI server (main.py).

Covers:
- GET  /health                     → health check
- GET  /.well-known/agent.json     → A2A agent card discovery
- POST /a2a  message/send          → synchronous A2A response
- POST /a2a  message/stream        → SSE streaming A2A response
- POST /a2a  unknown method        → JSON-RPC error
- Helper functions: _extract_user_text, _jsonrpc_error, _sse
- Concurrency semaphore configuration
- AGENT_CARD structure
"""

from __future__ import annotations

import asyncio
import json
import importlib
import sys
import types
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient


# ---------------------------------------------------------------------------
# Helpers – import main with mocked agent
# ---------------------------------------------------------------------------


def _get_main_module():
    """Return the ``main`` module, reloading it fresh."""
    import main as _main
    return importlib.reload(_main)


@pytest.fixture()
def main_mod():
    """Provide a freshly-reloaded ``main`` module."""
    return _get_main_module()


# ---------------------------------------------------------------------------
# Mock agent fixture – injects a fake agent into main._pizza_agent
# ---------------------------------------------------------------------------


@pytest.fixture()
def mock_agent(main_mod):
    """Create a mock agent and patch it into the module."""
    agent = MagicMock()
    # Synchronous run → returns a response with messages
    mock_response = MagicMock()
    mock_msg = MagicMock()
    mock_msg.text = "Here is your pizza info!"
    mock_response.messages = [mock_msg]
    agent.run = AsyncMock(return_value=mock_response)

    main_mod._pizza_agent = agent
    yield agent
    main_mod._pizza_agent = None


# ---------------------------------------------------------------------------
# Async FastAPI test client
# ---------------------------------------------------------------------------


@pytest_asyncio.fixture()
async def client(main_mod, mock_agent):
    """Create an ``httpx.AsyncClient`` bound to the FastAPI app.

    We skip the lifespan so we can inject the mock agent directly.
    """
    # Patch add_agent_framework_fastapi_endpoint to a no-op so lifespan doesn't fail
    with patch.object(main_mod, "add_agent_framework_fastapi_endpoint"):
        transport = ASGITransport(app=main_mod.app)
        async with AsyncClient(transport=transport, base_url="http://testserver") as ac:
            yield ac


# ============================================================================
# Health Check
# ============================================================================


class TestHealthEndpoint:
    """Tests for ``GET /health``."""

    @pytest.mark.asyncio
    async def test_health_returns_200(self, client):
        r = await client.get("/health")
        assert r.status_code == 200

    @pytest.mark.asyncio
    async def test_health_body_fields(self, client):
        r = await client.get("/health")
        data = r.json()
        assert data["status"] == "healthy"
        assert data["agent"] == "pizza-agent"
        assert "ag-ui" in data["protocols"]
        assert "a2a" in data["protocols"]
        assert data["streaming"] is True
        assert data["max_concurrent_requests"] == 500


# ============================================================================
# Agent Card Discovery
# ============================================================================


class TestAgentCard:
    """Tests for ``GET /.well-known/agent.json``."""

    @pytest.mark.asyncio
    async def test_agent_card_returns_200(self, client):
        r = await client.get("/.well-known/agent.json")
        assert r.status_code == 200

    @pytest.mark.asyncio
    async def test_agent_card_name(self, client):
        r = await client.get("/.well-known/agent.json")
        data = r.json()
        assert data["name"] == "pizza-agent"

    @pytest.mark.asyncio
    async def test_agent_card_url_populated(self, client):
        r = await client.get("/.well-known/agent.json")
        data = r.json()
        assert data["url"].endswith("/a2a")

    @pytest.mark.asyncio
    async def test_agent_card_capabilities(self, client):
        r = await client.get("/.well-known/agent.json")
        data = r.json()
        assert data["capabilities"]["streaming"] is True

    @pytest.mark.asyncio
    async def test_agent_card_skills_count(self, client):
        r = await client.get("/.well-known/agent.json")
        data = r.json()
        assert len(data["skills"]) == 4
        skill_ids = {s["id"] for s in data["skills"]}
        assert skill_ids == {"order-pizza", "track-order", "browse-menu", "get-specials"}


# ============================================================================
# A2A – message/send
# ============================================================================


class TestA2AMessageSend:
    """Tests for ``POST /a2a`` with method ``message/send``."""

    @pytest.mark.asyncio
    async def test_message_send_success(self, client, mock_agent):
        payload = {
            "jsonrpc": "2.0",
            "id": "req-1",
            "method": "message/send",
            "params": {
                "message": {
                    "role": "user",
                    "parts": [{"type": "text", "text": "Show me the menu"}],
                }
            },
        }
        r = await client.post("/a2a", json=payload)
        assert r.status_code == 200
        data = r.json()
        assert data["jsonrpc"] == "2.0"
        assert data["id"] == "req-1"
        assert data["result"]["status"]["state"] == "completed"

    @pytest.mark.asyncio
    async def test_message_send_has_artifacts(self, client, mock_agent):
        payload = {
            "jsonrpc": "2.0",
            "id": "req-2",
            "method": "message/send",
            "params": {
                "message": {
                    "role": "user",
                    "parts": [{"type": "text", "text": "Order a Margherita"}],
                }
            },
        }
        r = await client.post("/a2a", json=payload)
        data = r.json()
        artifacts = data["result"]["artifacts"]
        assert len(artifacts) >= 1
        assert any(p["type"] == "text" for p in artifacts[0]["parts"])

    @pytest.mark.asyncio
    async def test_message_send_agent_called(self, client, mock_agent):
        payload = {
            "jsonrpc": "2.0",
            "id": "req-3",
            "method": "message/send",
            "params": {
                "message": {
                    "role": "user",
                    "parts": [{"type": "text", "text": "Track my order"}],
                }
            },
        }
        await client.post("/a2a", json=payload)
        mock_agent.run.assert_awaited_once_with("Track my order")

    @pytest.mark.asyncio
    async def test_message_send_agent_error(self, client, mock_agent):
        mock_agent.run = AsyncMock(side_effect=RuntimeError("LLM timeout"))
        payload = {
            "jsonrpc": "2.0",
            "id": "req-err",
            "method": "message/send",
            "params": {
                "message": {
                    "role": "user",
                    "parts": [{"type": "text", "text": "Hello"}],
                }
            },
        }
        r = await client.post("/a2a", json=payload)
        data = r.json()
        assert "error" in data
        assert data["error"]["code"] == -32603

    @pytest.mark.asyncio
    async def test_message_send_agent_not_initialised(self, client, main_mod):
        main_mod._pizza_agent = None
        payload = {
            "jsonrpc": "2.0",
            "id": "req-nil",
            "method": "message/send",
            "params": {"message": {"role": "user", "parts": [{"type": "text", "text": "Hi"}]}},
        }
        r = await client.post("/a2a", json=payload)
        data = r.json()
        assert "error" in data
        assert "not initialised" in data["error"]["message"]


# ============================================================================
# A2A – message/stream
# ============================================================================


class TestA2AMessageStream:
    """Tests for ``POST /a2a`` with method ``message/stream``."""

    @pytest.mark.asyncio
    async def test_message_stream_returns_sse(self, client, mock_agent):
        # Set up a streaming mock
        mock_content = MagicMock()
        mock_content.text = "Streaming pizza info"
        mock_update = MagicMock()
        mock_update.contents = [mock_content]

        async def _aiter(*_args, **_kwargs):
            yield mock_update

        mock_stream_ctx = MagicMock()
        mock_stream_obj = MagicMock()
        mock_stream_obj.__aiter__ = _aiter
        mock_stream_ctx.__aenter__ = AsyncMock(return_value=mock_stream_obj)
        mock_stream_ctx.__aexit__ = AsyncMock(return_value=False)
        mock_agent.run = MagicMock(return_value=mock_stream_ctx)

        payload = {
            "jsonrpc": "2.0",
            "id": "stream-1",
            "method": "message/stream",
            "params": {
                "message": {
                    "role": "user",
                    "parts": [{"type": "text", "text": "Show me specials"}],
                }
            },
        }
        r = await client.post("/a2a", json=payload)
        assert r.status_code == 200
        assert "text/event-stream" in r.headers.get("content-type", "")

    @pytest.mark.asyncio
    async def test_message_stream_agent_not_initialised(self, client, main_mod):
        main_mod._pizza_agent = None
        payload = {
            "jsonrpc": "2.0",
            "id": "stream-nil",
            "method": "message/stream",
            "params": {"message": {"role": "user", "parts": [{"type": "text", "text": "Hi"}]}},
        }
        r = await client.post("/a2a", json=payload)
        assert r.status_code == 200  # SSE stream always 200
        body = r.text
        assert "not initialised" in body


# ============================================================================
# A2A – Unknown method
# ============================================================================


class TestA2AUnknownMethod:
    """Tests for ``POST /a2a`` with an unsupported JSON-RPC method."""

    @pytest.mark.asyncio
    async def test_unknown_method_returns_error(self, client):
        payload = {
            "jsonrpc": "2.0",
            "id": "bad-1",
            "method": "task/execute",
            "params": {},
        }
        r = await client.post("/a2a", json=payload)
        data = r.json()
        assert "error" in data
        assert data["error"]["code"] == -32601
        assert "not found" in data["error"]["message"]


# ============================================================================
# Helper functions
# ============================================================================


class TestHelpers:
    """Tests for helper functions in main.py."""

    def test_extract_user_text_normal(self, main_mod):
        params = {
            "message": {
                "role": "user",
                "parts": [
                    {"type": "text", "text": "I want pepperoni"},
                ],
            }
        }
        assert main_mod._extract_user_text(params) == "I want pepperoni"

    def test_extract_user_text_multiple_parts(self, main_mod):
        params = {
            "message": {
                "role": "user",
                "parts": [
                    {"type": "text", "text": "I want"},
                    {"type": "text", "text": "pepperoni"},
                ],
            }
        }
        assert main_mod._extract_user_text(params) == "I want pepperoni"

    def test_extract_user_text_empty_defaults(self, main_mod):
        params = {"message": {"parts": []}}
        assert main_mod._extract_user_text(params) == "Hello"

    def test_extract_user_text_no_message(self, main_mod):
        assert main_mod._extract_user_text({}) == "Hello"

    def test_extract_user_text_mixed_types(self, main_mod):
        params = {
            "message": {
                "parts": [
                    {"type": "image", "url": "http://..."},
                    {"type": "text", "text": "Describe this"},
                ],
            }
        }
        assert main_mod._extract_user_text(params) == "Describe this"

    def test_jsonrpc_error_format(self, main_mod):
        resp = main_mod._jsonrpc_error("id-42", -32600, "Invalid request")
        data = json.loads(resp.body)
        assert data["jsonrpc"] == "2.0"
        assert data["id"] == "id-42"
        assert data["error"]["code"] == -32600
        assert data["error"]["message"] == "Invalid request"

    def test_sse_format(self, main_mod):
        payload = {"key": "value"}
        result = main_mod._sse(payload)
        assert result.startswith("data: ")
        assert result.endswith("\n\n")
        parsed = json.loads(result[len("data: ") :].strip())
        assert parsed == payload


# ============================================================================
# AGENT_CARD structure
# ============================================================================


class TestAgentCardStructure:
    """Validate the static AGENT_CARD dict in main.py."""

    def test_card_has_required_fields(self, main_mod):
        required = {"name", "description", "version", "url", "capabilities", "skills"}
        assert required.issubset(main_mod.AGENT_CARD.keys())

    def test_card_name(self, main_mod):
        assert main_mod.AGENT_CARD["name"] == "pizza-agent"

    def test_card_streaming_capability(self, main_mod):
        assert main_mod.AGENT_CARD["capabilities"]["streaming"] is True

    def test_card_input_output_modes(self, main_mod):
        assert "text" in main_mod.AGENT_CARD["defaultInputModes"]
        assert "text" in main_mod.AGENT_CARD["defaultOutputModes"]


# ============================================================================
# Concurrency configuration
# ============================================================================


class TestConcurrency:
    """Verify concurrency limits are configured correctly."""

    def test_max_concurrent_is_500(self, main_mod):
        assert main_mod.MAX_CONCURRENT_REQUESTS == 500

    def test_semaphore_is_asyncio_semaphore(self, main_mod):
        assert isinstance(main_mod._request_semaphore, asyncio.Semaphore)
