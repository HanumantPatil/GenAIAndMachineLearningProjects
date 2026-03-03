# Copyright (c) Microsoft. All rights reserved.

"""Pizza Agent server – AG-UI + A2A dual-protocol entry point.

Endpoints
---------
- ``POST /ag-ui``                   AG-UI protocol (frontend / UI)
- ``POST /a2a``                     A2A JSON-RPC (agent-to-agent)
- ``GET  /.well-known/agent.json``  A2A agent card discovery
- ``GET  /health``                  Health check

Run
---
::

    # Development
    python main.py

    # Production (500 concurrent requests)
    uvicorn main:app --host 0.0.0.0 --port 8000 --limit-concurrency 500
"""

from __future__ import annotations

import asyncio
import json
import logging
import os
import uuid
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

import uvicorn
from agent_framework.ag_ui import add_agent_framework_fastapi_endpoint
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse

from agent import create_foundry_pizza_agent, create_pizza_agent

load_dotenv(override=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Concurrency gate – hard-caps in-flight requests to 500
# ---------------------------------------------------------------------------
MAX_CONCURRENT_REQUESTS = 500
_request_semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)

# ---------------------------------------------------------------------------
# A2A Agent Card (returned by /.well-known/agent.json)
# ---------------------------------------------------------------------------
AGENT_CARD: dict[str, Any] = {
    "name": "pizza-agent",
    "description": (
        "AI-powered pizza ordering assistant. "
        "Handles menu browsing, order placement, tracking, specials, and cancellations."
    ),
    "version": "1.0.0",
    "url": "",  # populated dynamically per request
    "capabilities": {
        "streaming": True,
        "pushNotifications": False,
    },
    "skills": [
        {
            "id": "order-pizza",
            "name": "Order Pizza",
            "description": "Place pizza orders with customisation options",
        },
        {
            "id": "track-order",
            "name": "Track Order",
            "description": "Track the status of pizza orders",
        },
        {
            "id": "browse-menu",
            "name": "Browse Menu",
            "description": "View the pizza menu with prices and descriptions",
        },
        {
            "id": "get-specials",
            "name": "Get Specials",
            "description": "Get today's pizza specials and promotions",
        },
    ],
    "defaultInputModes": ["text"],
    "defaultOutputModes": ["text"],
}

# ---------------------------------------------------------------------------
# Application lifespan – agent initialisation & cleanup
# ---------------------------------------------------------------------------

# Module-level holder so endpoints can reference the agent.
_pizza_agent = None
_foundry_cleanup: list = []  # (credential, provider) to close on shutdown


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialise the pizza-agent (local *or* Foundry) before accepting traffic."""
    global _pizza_agent

    use_foundry = os.getenv("USE_FOUNDRY_AGENT", "false").lower() == "true"

    if use_foundry:
        agent, credential, provider = await create_foundry_pizza_agent()
        _pizza_agent = agent
        _foundry_cleanup.extend([credential, provider])
    else:
        _pizza_agent = create_pizza_agent()

    # Register the AG-UI endpoint *after* the agent is ready.
    add_agent_framework_fastapi_endpoint(
        app=app,
        agent=_pizza_agent,
        path="/ag-ui",
    )
    logger.info("AG-UI endpoint registered at POST /ag-ui")

    yield  # ---------- app is running ----------

    # Cleanup Foundry resources if any
    for resource in reversed(_foundry_cleanup):
        try:
            await resource.close()
        except Exception:
            logger.warning("Failed to close Foundry resource", exc_info=True)

    logger.info("pizza-agent server shut down")


# ---------------------------------------------------------------------------
# FastAPI application
# ---------------------------------------------------------------------------

app = FastAPI(
    title="Pizza Agent",
    description="AI-powered pizza ordering agent supporting AG-UI and A2A protocols",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================================
# A2A Protocol: Agent Card Discovery
# ============================================================================


@app.get("/.well-known/agent.json", tags=["A2A"])
async def get_agent_card(request: Request) -> JSONResponse:
    """Return the A2A agent card for discovery by other agents."""
    card = AGENT_CARD.copy()
    card["url"] = str(request.base_url).rstrip("/") + "/a2a"
    return JSONResponse(content=card)


# ============================================================================
# A2A Protocol: JSON-RPC Endpoint
# ============================================================================


@app.post("/a2a", tags=["A2A"], response_model=None)
async def a2a_endpoint(request: Request) -> JSONResponse | StreamingResponse:
    """A2A JSON-RPC endpoint supporting ``message/send`` and ``message/stream``."""
    async with _request_semaphore:
        body = await request.json()
        method: str = body.get("method", "")
        params: dict = body.get("params", {})
        req_id: str = body.get("id", str(uuid.uuid4()))

        if method == "message/send":
            return await _a2a_message_send(params, req_id)
        elif method == "message/stream":
            return _a2a_message_stream(params, req_id)
        else:
            return _jsonrpc_error(req_id, -32601, f"Method '{method}' not found")


# ---- message/send (synchronous) ------------------------------------------


async def _a2a_message_send(params: dict, req_id: str) -> JSONResponse:
    if _pizza_agent is None:
        return _jsonrpc_error(req_id, -32603, "Agent not initialised")

    user_text = _extract_user_text(params)
    try:
        response = await _pizza_agent.run(user_text)

        parts = []
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
        return _jsonrpc_error(req_id, -32603, str(exc))


# ---- message/stream (SSE) ------------------------------------------------


def _a2a_message_stream(params: dict, req_id: str) -> StreamingResponse:
    async def _generate() -> AsyncGenerator[str, None]:
        if _pizza_agent is None:
            yield _sse({"jsonrpc": "2.0", "id": req_id, "error": {"code": -32603, "message": "Agent not initialised"}})
            return

        user_text = _extract_user_text(params)
        task_id = str(uuid.uuid4())

        # Working status
        yield _sse(
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
            # Stream the agent response
            # ResponseStream supports async iteration but NOT async context manager
            stream = _pizza_agent.run(user_text, stream=True)
            async for update in stream:
                text = update.text
                if text:
                    yield _sse(
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
            yield _sse({"jsonrpc": "2.0", "id": req_id, "error": {"code": -32603, "message": str(exc)}})
            return

        # Completed
        yield _sse(
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


# ============================================================================
# Health Check
# ============================================================================


@app.get("/health", tags=["Ops"])
async def health_check():
    """Lightweight health probe."""
    return {
        "status": "healthy",
        "agent": "pizza-agent",
        "protocols": ["ag-ui", "a2a"],
        "streaming": True,
        "max_concurrent_requests": MAX_CONCURRENT_REQUESTS,
    }


# ============================================================================
# Helpers
# ============================================================================


def _extract_user_text(params: dict) -> str:
    """Pull plain-text content from an A2A ``message/send`` or ``message/stream`` payload."""
    message = params.get("message", {})
    parts = message.get("parts", [])
    texts = [p.get("text", "") for p in parts if p.get("type") == "text"]
    return " ".join(texts).strip() or "Hello"


def _jsonrpc_error(req_id: str, code: int, message: str) -> JSONResponse:
    return JSONResponse(
        content={"jsonrpc": "2.0", "id": req_id, "error": {"code": code, "message": message}}
    )


def _sse(payload: dict) -> str:
    """Format a dict as a single Server-Sent Event data frame."""
    return f"data: {json.dumps(payload)}\n\n"


# ============================================================================
# CLI entry point
# ============================================================================


def main() -> None:
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    workers = int(os.getenv("WORKERS", "1"))

    logger.info("=" * 60)
    logger.info("  pizza-agent server")
    logger.info("=" * 60)
    logger.info("  AG-UI endpoint : POST http://%s:%s/ag-ui", host, port)
    logger.info("  A2A endpoint   : POST http://%s:%s/a2a", host, port)
    logger.info("  Agent Card     : GET  http://%s:%s/.well-known/agent.json", host, port)
    logger.info("  Health         : GET  http://%s:%s/health", host, port)
    logger.info("  Workers        : %s", workers)
    logger.info("  Concurrency    : %s", MAX_CONCURRENT_REQUESTS)
    logger.info("=" * 60)

    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        workers=workers,
        log_level="info",
        limit_concurrency=MAX_CONCURRENT_REQUESTS,
        timeout_keep_alive=30,
        access_log=True,
    )


if __name__ == "__main__":
    main()
