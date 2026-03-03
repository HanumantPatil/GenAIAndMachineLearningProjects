# Copyright (c) Microsoft. All rights reserved.

"""AG-UI Protocol Client – test the pizza-agent via Server-Sent Events.

The AG-UI protocol uses ``POST /ag-ui`` and returns an SSE stream.
This client demonstrates sending messages and consuming the streamed
agent responses in real-time.

Usage
-----
::

    # Start the server first:
    python main.py

    # Then run the client:
    python client_agui.py
    python client_agui.py --base-url http://localhost:9000
"""

from __future__ import annotations

import argparse
import json
import sys
import uuid

import httpx

# ---------------------------------------------------------------------------
# Defaults
# ---------------------------------------------------------------------------

DEFAULT_BASE_URL = "http://localhost:8000"
AGUI_PATH = "/ag-ui"
TIMEOUT = 60.0


# ---------------------------------------------------------------------------
# Helper – build an AG-UI message payload
# ---------------------------------------------------------------------------


def _agui_payload(text: str, thread_id: str | None = None) -> dict:
    """Build a payload for the AG-UI endpoint.

    The AG-UI protocol accepts messages via POST with SSE streaming back.
    The exact schema depends on the ``agent-framework-ag-ui`` implementation;
    this mirrors the typical ``RunAgentInput`` shape.
    """
    return {
        "thread_id": thread_id or str(uuid.uuid4()),
        "run_id": str(uuid.uuid4()),
        "messages": [
            {
                "id": str(uuid.uuid4()),
                "role": "user",
                "content": text,
            }
        ],
    }


# ============================================================================
# Stream an AG-UI request
# ============================================================================


def stream_agui(base_url: str, text: str, thread_id: str | None = None) -> str | None:
    """Send a message to the AG-UI endpoint and stream the response.

    Args:
        base_url: Server base URL.
        text: User message to send.
        thread_id: Optional thread ID for multi-turn conversations.

    Returns:
        The thread_id used (for follow-up messages), or None on failure.
    """
    url = f"{base_url}{AGUI_PATH}"
    payload = _agui_payload(text, thread_id)
    tid = payload["thread_id"]

    print("-" * 60)
    print(f"  [AG-UI Stream] User: {text}")
    print(f"  Thread: {tid}")
    print("-" * 60)

    try:
        with httpx.stream("POST", url, json=payload, timeout=TIMEOUT) as resp:
            resp.raise_for_status()
            buffer = ""
            event_count = 0
            full_text_parts: list[str] = []

            for chunk in resp.iter_text():
                buffer += chunk

                # Parse SSE frames separated by double newlines
                while "\n\n" in buffer:
                    frame, buffer = buffer.split("\n\n", 1)
                    event_type, data = _parse_sse_frame(frame)
                    if data is not None:
                        event_count += 1
                        _print_agui_event(event_type, data, event_count, full_text_parts)

            # Flush remaining buffer
            if buffer.strip():
                event_type, data = _parse_sse_frame(buffer.strip())
                if data is not None:
                    event_count += 1
                    _print_agui_event(event_type, data, event_count, full_text_parts)

            print()
            if full_text_parts:
                print("  --- Full Response ---")
                print(f"  {''.join(full_text_parts)}")
            print(f"  --- Stream completed ({event_count} events) ---")
            print()
            return tid

    except httpx.HTTPError as exc:
        print(f"  ERROR: {exc}")
        print()
        return None


# ---------------------------------------------------------------------------
# SSE frame parsing
# ---------------------------------------------------------------------------


def _parse_sse_frame(frame: str) -> tuple[str, dict | str | None]:
    """Parse a single SSE frame into (event_type, data)."""
    event_type = "message"
    data_lines: list[str] = []

    for line in frame.splitlines():
        if line.startswith("event: "):
            event_type = line[len("event: "):].strip()
        elif line.startswith("data: "):
            data_lines.append(line[len("data: "):])
        elif line.startswith("data:"):
            data_lines.append(line[len("data:"):])

    if not data_lines:
        return event_type, None

    raw = "\n".join(data_lines)
    try:
        return event_type, json.loads(raw)
    except json.JSONDecodeError:
        return event_type, raw


def _print_agui_event(
    event_type: str,
    data: dict | str,
    idx: int,
    full_text_parts: list[str],
) -> None:
    """Pretty-print an AG-UI SSE event."""
    if isinstance(data, str):
        print(f"  Event #{idx} [{event_type}]: {data}")
        return

    # Handle common AG-UI event types
    if event_type in ("TEXT_MESSAGE_CONTENT", "text_message_content"):
        delta = data.get("delta", "")
        if delta:
            full_text_parts.append(delta)
            print(f"  Event #{idx} [TEXT_DELTA]: {delta}", end="")
        return

    if event_type in ("TEXT_MESSAGE_START", "text_message_start"):
        role = data.get("role", "agent")
        print(f"  Event #{idx} [MSG_START] role={role}")
        return

    if event_type in ("TEXT_MESSAGE_END", "text_message_end"):
        print()
        print(f"  Event #{idx} [MSG_END]")
        return

    if event_type in ("RUN_STARTED", "run_started"):
        run_id = data.get("run_id", data.get("runId", ""))
        print(f"  Event #{idx} [RUN_STARTED] run_id={run_id}")
        return

    if event_type in ("RUN_FINISHED", "run_finished"):
        print(f"  Event #{idx} [RUN_FINISHED]")
        return

    if event_type in ("RUN_ERROR", "run_error"):
        msg = data.get("message", data.get("error", str(data)))
        print(f"  Event #{idx} [RUN_ERROR]: {msg}")
        return

    if event_type in ("TOOL_CALL_START", "tool_call_start"):
        name = data.get("name", data.get("tool_name", ""))
        print(f"  Event #{idx} [TOOL_CALL_START] tool={name}")
        return

    if event_type in ("TOOL_CALL_END", "tool_call_end"):
        print(f"  Event #{idx} [TOOL_CALL_END]")
        return

    if event_type in ("TOOL_CALL_ARGS", "tool_call_args"):
        delta = data.get("delta", "")
        if delta:
            print(f"  Event #{idx} [TOOL_ARGS]: {delta}")
        return

    # Generic fallback
    preview = json.dumps(data)[:120]
    print(f"  Event #{idx} [{event_type}]: {preview}")


# ============================================================================
# Health Check
# ============================================================================


def check_health(base_url: str) -> bool:
    """Verify the server is running."""
    try:
        resp = httpx.get(f"{base_url}/health", timeout=5)
        resp.raise_for_status()
        data = resp.json()
        print(f"  Health: {data.get('status')} | Agent: {data.get('agent')}")
        protocols = data.get("protocols", [])
        if "ag-ui" not in protocols:
            print("  WARNING: AG-UI protocol not listed in health response")
        print()
        return data.get("status") == "healthy"
    except httpx.HTTPError:
        print("  Server is not reachable. Start the server first: python main.py")
        return False


# ============================================================================
# Demo – predefined conversation flow
# ============================================================================


def run_demo(base_url: str) -> None:
    """Run the full AG-UI client demo with a multi-turn conversation."""
    print()
    print("*" * 60)
    print("  Pizza Agent – AG-UI Protocol Client")
    print("*" * 60)
    print()

    if not check_health(base_url):
        sys.exit(1)

    # Single-thread multi-turn conversation
    print("=" * 60)
    print("  Multi-turn Streaming Conversation")
    print("=" * 60)
    print()

    # Turn 1 – Browse menu
    tid = stream_agui(base_url, "Hi! Show me the pizza menu")

    # Turn 2 – Ask about specials
    stream_agui(base_url, "What specials do you have today?", thread_id=tid)

    # Turn 3 – Place an order
    stream_agui(
        base_url,
        "I'll have 2 large Pepperoni pizzas and 1 medium Veggie Supreme",
        thread_id=tid,
    )

    # Turn 4 – Track order
    stream_agui(base_url, "Can you track my order?", thread_id=tid)

    # Turn 5 – Cancel order
    stream_agui(base_url, "Actually, cancel my order please", thread_id=tid)

    # Separate thread – new conversation
    print("=" * 60)
    print("  New Conversation (separate thread)")
    print("=" * 60)
    print()

    stream_agui(base_url, "What's the cheapest pizza you have? I'm on a budget")
    stream_agui(base_url, "Order a small Margherita with extra basil")


def run_interactive(base_url: str) -> None:
    """Run an interactive AG-UI chat session with the pizza agent."""
    print()
    print("*" * 60)
    print("  Pizza Agent – AG-UI Interactive Chat")
    print("  Type 'quit' to exit, 'new' for a new conversation")
    print("*" * 60)
    print()

    if not check_health(base_url):
        sys.exit(1)

    thread_id: str | None = None
    print("  Starting new conversation...")
    print()

    while True:
        try:
            user_input = input("  You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n  Goodbye!")
            break

        if not user_input:
            continue
        if user_input.lower() == "quit":
            print("  Goodbye!")
            break
        if user_input.lower() == "new":
            thread_id = None
            print("  --- New conversation started ---")
            print()
            continue

        thread_id = stream_agui(base_url, user_input, thread_id=thread_id)


# ============================================================================
# CLI
# ============================================================================


def main() -> None:
    parser = argparse.ArgumentParser(description="AG-UI Protocol Client for pizza-agent")
    parser.add_argument(
        "--base-url",
        default=DEFAULT_BASE_URL,
        help=f"Server base URL (default: {DEFAULT_BASE_URL})",
    )
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Run in interactive chat mode instead of the demo",
    )
    args = parser.parse_args()

    if args.interactive:
        run_interactive(args.base_url)
    else:
        run_demo(args.base_url)


if __name__ == "__main__":
    main()
