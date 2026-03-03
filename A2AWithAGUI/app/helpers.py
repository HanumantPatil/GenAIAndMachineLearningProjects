# Copyright (c) Microsoft. All rights reserved.

"""A2A protocol helper functions.

Provides formatting utilities for JSON-RPC responses and
Server-Sent Events used by the A2A endpoint handlers.
"""

from __future__ import annotations

import json

from fastapi.responses import JSONResponse


def extract_user_text(params: dict) -> str:
    """Pull plain-text content from an A2A ``message/send`` or ``message/stream`` payload."""
    message = params.get("message", {})
    parts = message.get("parts", [])
    texts = [p.get("text", "") for p in parts if p.get("type") == "text"]
    return " ".join(texts).strip() or "Hello"


def jsonrpc_error(req_id: str, code: int, message: str) -> JSONResponse:
    """Return a JSON-RPC 2.0 error response."""
    return JSONResponse(
        content={
            "jsonrpc": "2.0",
            "id": req_id,
            "error": {"code": code, "message": message},
        }
    )


def sse(payload: dict) -> str:
    """Format a dict as a single Server-Sent Event data frame."""
    return f"data: {json.dumps(payload)}\n\n"
