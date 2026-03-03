# Copyright (c) Microsoft. All rights reserved.

"""A2A protocol routes – agent card discovery and JSON-RPC endpoint.

Endpoints
---------
- ``GET  /.well-known/agent.json``  — Agent card for A2A discovery
- ``POST /a2a``                      — JSON-RPC: ``message/send`` and ``message/stream``
"""

from __future__ import annotations

import logging
import uuid
from collections.abc import AsyncGenerator
from typing import Any

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse, StreamingResponse

from app import state
from app.agent_card import AGENT_CARD
from app.helpers import extract_user_text, jsonrpc_error, sse

logger = logging.getLogger(__name__)

router = APIRouter(tags=["A2A"])


# ============================================================================
# Agent Card Discovery
# ============================================================================


@router.get("/.well-known/agent.json")
async def get_agent_card(request: Request) -> JSONResponse:
    """Return the A2A agent card for discovery by other agents."""
    card = AGENT_CARD.copy()
    card["url"] = str(request.base_url).rstrip("/") + "/a2a"
    return JSONResponse(content=card)


# ============================================================================
# JSON-RPC Endpoint
# ============================================================================


@router.post("/a2a", response_model=None)
async def a2a_endpoint(request: Request) -> JSONResponse | StreamingResponse:
    """A2A JSON-RPC endpoint supporting ``message/send`` and ``message/stream``."""
    async with state.request_semaphore:
        body = await request.json()
        method: str = body.get("method", "")
        params: dict = body.get("params", {})
        req_id: str = body.get("id", str(uuid.uuid4()))

        if method == "message/send":
            return await _a2a_message_send(params, req_id)
        elif method == "message/stream":
            return _a2a_message_stream(params, req_id)
        else:
            return jsonrpc_error(req_id, -32601, f"Method '{method}' not found")


# ---- message/send (synchronous) ------------------------------------------


async def _a2a_message_send(params: dict, req_id: str) -> JSONResponse:
    """Handle a synchronous A2A ``message/send`` request."""
    if state.pizza_agent is None:
        return jsonrpc_error(req_id, -32603, "Agent not initialised")

    user_text = extract_user_text(params)
    try:
        response = await state.pizza_agent.run(user_text)

        parts: list[dict[str, Any]] = []
        for msg in response.messages:
            if msg.text:
                parts.append({"type": "text", "text": msg.text})

        return JSONResponse(
            content={
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "id": str(uuid.uuid4()),
                    "status": {"state": "completed"},
                    "artifacts": [{"parts": parts}],
                },
            }
        )
    except Exception as exc:
        logger.exception("A2A message/send failed")
        return jsonrpc_error(req_id, -32603, str(exc))


# ---- message/stream (SSE) ------------------------------------------------


def _a2a_message_stream(params: dict, req_id: str) -> StreamingResponse:
    """Handle an SSE-streaming A2A ``message/stream`` request."""

    async def _generate() -> AsyncGenerator[str, None]:
        if state.pizza_agent is None:
            yield sse(
                {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {"code": -32603, "message": "Agent not initialised"},
                }
            )
            return

        user_text = extract_user_text(params)
        task_id = str(uuid.uuid4())

        # Working status
        yield sse(
            {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "id": task_id,
                    "status": {
                        "state": "working",
                        "message": {
                            "role": "agent",
                            "parts": [{"type": "text", "text": "Processing your request..."}],
                        },
                    },
                },
            }
        )

        try:
            # ResponseStream supports async iteration but NOT async context manager
            stream = state.pizza_agent.run(user_text, stream=True)
            async for update in stream:
                text = update.text
                if text:
                    yield sse(
                        {
                            "jsonrpc": "2.0",
                            "id": req_id,
                            "result": {
                                "id": task_id,
                                "status": {
                                    "state": "working",
                                    "message": {
                                        "role": "agent",
                                        "parts": [{"type": "text", "text": text}],
                                    },
                                },
                            },
                        }
                    )
        except Exception as exc:
            logger.exception("A2A message/stream failed")
            yield sse(
                {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {"code": -32603, "message": str(exc)},
                }
            )
            return

        # Completed
        yield sse(
            {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {"id": task_id, "status": {"state": "completed"}},
            }
        )

    return StreamingResponse(
        _generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )
