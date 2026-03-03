# Copyright (c) Microsoft. All rights reserved.

"""A2A Protocol Client – test the pizza-agent via JSON-RPC.

Demonstrates
------------
1. Agent card discovery  (GET ``/.well-known/agent.json``)
2. Synchronous request   (``message/send``)
3. Streaming request     (``message/stream`` → SSE)

Usage
-----
::

    # Start the server first:
    python main.py

    # Then run the client:
    python client_a2a.py
    python client_a2a.py --base-url http://localhost:9000
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
TIMEOUT = 60.0  # seconds


# ---------------------------------------------------------------------------
# Helper – build a JSON-RPC request payload
# ---------------------------------------------------------------------------


def _jsonrpc_request(method: str, text: str) -> dict:
    """Build a JSON-RPC 2.0 request for the A2A endpoint."""
    return {
        "jsonrpc": "2.0",
        "id": str(uuid.uuid4()),
        "method": method,
        "params": {
            "message": {
                "role": "user",
                "parts": [{"type": "text", "text": text}],
            }
        },
    }


# ============================================================================
# 1. Agent Card Discovery
# ============================================================================


def discover_agent(base_url: str) -> dict | None:
    """Fetch the A2A agent card from ``/.well-known/agent.json``."""
    url = f"{base_url}/.well-known/agent.json"
    print("=" * 60)
    print("  A2A Agent Card Discovery")
    print("=" * 60)
    print(f"  GET {url}")
    print()

    try:
        resp = httpx.get(url, timeout=TIMEOUT)
        resp.raise_for_status()
        card = resp.json()

        print(f"  Name        : {card.get('name')}")
        print(f"  Description : {card.get('description')}")
        print(f"  Version     : {card.get('version')}")
        print(f"  URL         : {card.get('url')}")
        print(f"  Streaming   : {card.get('capabilities', {}).get('streaming')}")
        skills = card.get("skills", [])
        if skills:
            print(f"  Skills      : {len(skills)}")
            for s in skills:
                print(f"    - {s['name']}: {s['description']}")
        print()
        return card
    except httpx.HTTPError as exc:
        print(f"  ERROR: {exc}")
        return None


# ============================================================================
# 2. Synchronous Request (message/send)
# ============================================================================


def send_message(base_url: str, text: str) -> dict | None:
    """Send a synchronous ``message/send`` request to the A2A endpoint."""
    url = f"{base_url}/a2a"
    payload = _jsonrpc_request("message/send", text)

    print("-" * 60)
    print(f"  [message/send] User: {text}")
    print("-" * 60)

    try:
        resp = httpx.post(url, json=payload, timeout=TIMEOUT)
        resp.raise_for_status()
        data = resp.json()

        # Extract agent reply
        result = data.get("result", {})
        status = result.get("status", {}).get("state", "unknown")
        artifacts = result.get("artifacts", [])

        print(f"  Status: {status}")
        for artifact in artifacts:
            for part in artifact.get("parts", []):
                if part.get("type") == "text":
                    print(f"  Agent : {part['text']}")
        print()
        return data
    except httpx.HTTPError as exc:
        print(f"  ERROR: {exc}")
        return None


# ============================================================================
# 3. Streaming Request (message/stream)
# ============================================================================


def stream_message(base_url: str, text: str) -> None:
    """Send a ``message/stream`` request and consume the SSE stream."""
    url = f"{base_url}/a2a"
    payload = _jsonrpc_request("message/stream", text)

    print("-" * 60)
    print(f"  [message/stream] User: {text}")
    print("-" * 60)

    try:
        with httpx.stream("POST", url, json=payload, timeout=TIMEOUT) as resp:
            resp.raise_for_status()
            buffer = ""
            event_count = 0

            for chunk in resp.iter_text():
                buffer += chunk
                # Parse SSE frames: "data: {...}\n\n"
                while "\n\n" in buffer:
                    frame, buffer = buffer.split("\n\n", 1)
                    for line in frame.strip().splitlines():
                        if line.startswith("data: "):
                            raw = line[len("data: "):]
                            try:
                                event = json.loads(raw)
                                event_count += 1
                                _print_stream_event(event, event_count)
                            except json.JSONDecodeError:
                                print(f"  [raw] {raw}")

            # Handle any remaining data in buffer
            if buffer.strip():
                for line in buffer.strip().splitlines():
                    if line.startswith("data: "):
                        raw = line[len("data: "):]
                        try:
                            event = json.loads(raw)
                            event_count += 1
                            _print_stream_event(event, event_count)
                        except json.JSONDecodeError:
                            pass

            print(f"  --- Stream completed ({event_count} events) ---")
            print()

    except httpx.HTTPError as exc:
        print(f"  ERROR: {exc}")


def _print_stream_event(event: dict, idx: int) -> None:
    """Pretty-print a single SSE event from the A2A stream."""
    if "error" in event:
        err = event["error"]
        print(f"  Event #{idx} [ERROR] code={err.get('code')} msg={err.get('message')}")
        return

    result = event.get("result", {})
    state = result.get("status", {}).get("state", "")
    message = result.get("status", {}).get("message", {})
    parts = message.get("parts", [])
    text = " ".join(p.get("text", "") for p in parts if p.get("type") == "text").strip()

    if text:
        print(f"  Event #{idx} [{state}]: {text}")
    else:
        print(f"  Event #{idx} [{state}]")


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
        print()
        return data.get("status") == "healthy"
    except httpx.HTTPError:
        print("  Server is not reachable. Start the server first: python main.py")
        return False


# ============================================================================
# Main – interactive demo
# ============================================================================


def run_demo(base_url: str) -> None:
    """Run the full A2A client demo."""
    print()
    print("*" * 60)
    print("  Pizza Agent – A2A Protocol Client")
    print("*" * 60)
    print()

    # Health check
    if not check_health(base_url):
        sys.exit(1)

    # 1. Discover agent card
    discover_agent(base_url)

    # 2. Synchronous requests (message/send)
    print("=" * 60)
    print("  Synchronous Requests (message/send)")
    print("=" * 60)
    print()

    send_message(base_url, "Show me the pizza menu")
    send_message(base_url, "What are today's specials?")
    send_message(base_url, "Order a large Pepperoni pizza please")
    send_message(base_url, "Can you track my order?")

    # 3. Streaming requests (message/stream)
    print("=" * 60)
    print("  Streaming Requests (message/stream)")
    print("=" * 60)
    print()

    stream_message(base_url, "Show me the full menu with descriptions")
    stream_message(base_url, "I'd like to order 2 medium BBQ Chicken pizzas with extra sauce")
    stream_message(base_url, "What specials do you have today? Also recommend a pizza for a party of 6")


def run_interactive(base_url: str) -> None:
    """Run an interactive chat session with the pizza agent via A2A."""
    print()
    print("*" * 60)
    print("  Pizza Agent – A2A Interactive Chat")
    print("  Type 'quit' to exit, 'stream' to toggle streaming")
    print("*" * 60)
    print()

    if not check_health(base_url):
        sys.exit(1)

    use_streaming = True
    print(f"  Mode: {'streaming' if use_streaming else 'synchronous'}")
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
        if user_input.lower() == "stream":
            use_streaming = not use_streaming
            print(f"  Mode: {'streaming' if use_streaming else 'synchronous'}")
            continue

        if use_streaming:
            stream_message(base_url, user_input)
        else:
            send_message(base_url, user_input)


# ============================================================================
# CLI
# ============================================================================


def main() -> None:
    parser = argparse.ArgumentParser(description="A2A Protocol Client for pizza-agent")
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
