# Pizza Agent – A2A + AG-UI Dual-Protocol Server

An AI-powered pizza ordering assistant built with the **Microsoft Agent Framework (Python SDK)**, supporting both the **A2A (Agent-to-Agent)** and **AG-UI (Agent-to-UI)** protocols with full streaming capabilities.

---

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Features](#features)
- [Project Structure](#project-structure)
- [Requirements Met](#requirements-met)
- [Setup](#setup)
- [Running the Server](#running-the-server)
- [Testing with Clients](#testing-with-clients)
- [Running Unit Tests](#running-unit-tests)
- [API Endpoints](#api-endpoints)
- [Pizza Menu & Tools](#pizza-menu--tools)
- [Configuration Reference](#configuration-reference)

---

## Overview

**pizza-agent** is a context-aware, streaming-enabled AI agent that handles pizza ordering workflows:

- Browse the menu, view today's specials
- Place orders with size/quantity customization
- Track and cancel orders in real-time
- Supports 500 concurrent requests
- Dual-protocol: works with both AI agents (A2A) and frontend UIs (AG-UI)

## Architecture

```text
┌──────────────┐     POST /ag-ui (SSE)      ┌─────────────────────────┐
│   AG-UI      │ ─────────────────────────── │                         │
│   Client     │                             │   FastAPI Server        │
└──────────────┘                             │                         │
                                             │  ┌───────────────────┐  │
┌──────────────┐     POST /a2a (JSON-RPC)    │  │   pizza-agent     │  │
│   A2A        │ ─────────────────────────── │  │                   │  │
│   Client     │                             │  │  Azure OpenAI /   │  │
└──────────────┘                             │  │  Foundry Backend  │  │
                                             │  └───────────────────┘  │
┌──────────────┐     GET /.well-known/       │                         │
│   Agent      │     agent.json              │  ┌───────────────────┐  │
│   Discovery  │ ─────────────────────────── │  │  5 Pizza Tools    │  │
└──────────────┘                             │  └───────────────────┘  │
                                             │                         │
                                             │  asyncio.Semaphore(500) │
                                             └─────────────────────────┘
```

## Features

| Feature | Description |
|---------|-------------|
| **A2A Protocol** | JSON-RPC endpoint with `message/send` (sync) and `message/stream` (SSE) |
| **AG-UI Protocol** | SSE streaming endpoint for frontend/UI integration |
| **Agent Card Discovery** | Standard `/.well-known/agent.json` for automatic agent discovery |
| **Streaming** | Real-time SSE streaming for both protocols |
| **500 Concurrent Requests** | `asyncio.Semaphore` + uvicorn `limit-concurrency` |
| **Context Awareness** | Agent remembers preferences and conversation history |
| **Foundry Integration** | Optional Azure AI Foundry hosted agent mode |
| **Speed Optimized** | Async I/O, connection pooling, lightweight in-memory stores |
| **5 Domain Tools** | Menu, ordering, tracking, specials, cancellation |

## Project Structure

```text
A2AWithAGUI/
├── main.py              # FastAPI server – dual-protocol endpoints
├── agent.py             # Agent creation (local + Foundry modes)
├── tools.py             # 5 pizza domain tools
├── client_a2a.py        # A2A protocol test client (sync + streaming)
├── client_agui.py       # AG-UI protocol test client (streaming)
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variable template
├── readme.md            # This file
├── .vscode/
│   └── launch.json      # VS Code debug configurations
└── tests/
    ├── __init__.py
    ├── conftest.py       # Shared fixtures & agent framework stubs
    ├── test_tools.py     # 47 tool tests
    ├── test_agent.py     # 14 agent configuration tests
    └── test_main.py      # 28 server endpoint tests
```

## Requirements Met

| # | Requirement | Implementation |
|---|-------------|----------------|
| 1 | **Python SDK** | Built entirely in Python 3.11+ |
| 2 | **Microsoft Agent Framework** | Uses `agent-framework-core`, `Agent`, `@tool`, `AzureOpenAIChatClient` |
| 3 | **A2A Protocol** | JSON-RPC endpoint at `POST /a2a` with agent card at `/.well-known/agent.json` |
| 4 | **AG-UI Protocol** | SSE endpoint at `POST /ag-ui` via `add_agent_framework_fastapi_endpoint()` |
| 5 | **Foundry Integration** | `create_foundry_pizza_agent()` uses `AzureAIProjectAgentProvider` (toggle via `USE_FOUNDRY_AGENT=true`) |
| 6 | **Streaming** | A2A `message/stream` → SSE, AG-UI → SSE, both with real-time token delivery |
| 7 | **500 Concurrent Requests** | `asyncio.Semaphore(500)` + uvicorn `limit-concurrency=500` |
| 8 | **Name: pizza-agent** | Agent name set in `Agent(name="pizza-agent", ...)` and agent card |
| 9 | **Speed Optimized** | Async handlers, in-memory stores, connection pooling, no blocking I/O |
| 10 | **Context Aware** | System prompt instructs agent to remember preferences; multi-turn supported |

## Setup

### Prerequisites

- Python 3.11+
- Azure OpenAI resource (endpoint + deployment)

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment

```bash
cp .env.example .env
```

Edit `.env` with your Azure OpenAI credentials:

```env
# Required
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_CHAT_DEPLOYMENT_NAME=gpt-4o

# One of these (API key OR DefaultAzureCredential):
AZURE_OPENAI_API_KEY=your-api-key-here

# Optional – Foundry mode
USE_FOUNDRY_AGENT=false
AZURE_AI_PROJECT_ENDPOINT=https://your-project.services.ai.azure.com

# Server
HOST=0.0.0.0
PORT=8000
WORKERS=1
```

## Running the Server

### Development Mode

```bash
python main.py
```

### Production Mode

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --limit-concurrency 500 --workers 4
```

### VS Code Debugger

Use the provided launch configurations in `.vscode/launch.json`:

- **Pizza Agent – Uvicorn**: Runs via uvicorn with reload
- **Pizza Agent – main.py**: Runs the main entry point directly

The server starts on `http://localhost:8000` by default.

## Testing with Clients

Two client scripts are provided for local testing. **Start the server first**, then run either client in a separate terminal.

### A2A Protocol Client

Tests agent card discovery, synchronous requests, and SSE streaming:

```bash
# Full demo (agent discovery + sync + streaming requests)
python client_a2a.py

# Interactive chat mode
python client_a2a.py --interactive

# Custom server URL
python client_a2a.py --base-url http://localhost:9000
```

**Demo mode** runs through:

1. Agent card discovery (`GET /.well-known/agent.json`)
2. Synchronous requests via `message/send` – menu, specials, ordering, tracking
3. Streaming requests via `message/stream` – menu browsing, complex orders, recommendations

**Interactive mode** provides a live chat where you can toggle between sync and streaming with the `stream` command.

### AG-UI Protocol Client

Tests SSE streaming with multi-turn conversations:

```bash
# Full demo (multi-turn conversation + new conversation)
python client_agui.py

# Interactive chat mode
python client_agui.py --interactive

# Custom server URL
python client_agui.py --base-url http://localhost:9000
```

**Demo mode** runs through:

1. Multi-turn conversation: menu → specials → order → track → cancel
2. Separate conversation thread: budget query → order with customization

**Interactive mode** provides a live chat. Type `new` to start a fresh conversation thread.

## Running Unit Tests

The project includes 89 unit tests covering tools, agent configuration, and server endpoints.

```bash
# Run all tests
pytest tests/ -v

# Run specific test files
pytest tests/test_tools.py -v      # 47 tool tests
pytest tests/test_agent.py -v      # 14 agent tests
pytest tests/test_main.py -v       # 28 server tests

# Run with coverage
pytest tests/ -v --tb=short
```

All tests use stubs for the Agent Framework SDK, so no Azure credentials are required.

## API Endpoints

### `GET /health`

Health check endpoint.

```bash
curl http://localhost:8000/health
```

```json
{
  "status": "healthy",
  "agent": "pizza-agent",
  "protocols": ["ag-ui", "a2a"],
  "streaming": true,
  "max_concurrent_requests": 500
}
```

### `GET /.well-known/agent.json`

A2A agent card for automatic discovery by other agents.

```bash
curl http://localhost:8000/.well-known/agent.json
```

Returns agent metadata including name, description, capabilities, skills, and the A2A endpoint URL.

### `POST /a2a`

A2A JSON-RPC endpoint supporting two methods:

**`message/send`** – Synchronous request/response:

```bash
curl -X POST http://localhost:8000/a2a \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": "1",
    "method": "message/send",
    "params": {
      "message": {
        "role": "user",
        "parts": [{"type": "text", "text": "Show me the menu"}]
      }
    }
  }'
```

**`message/stream`** – SSE streaming response:

```bash
curl -X POST http://localhost:8000/a2a \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": "1",
    "method": "message/stream",
    "params": {
      "message": {
        "role": "user",
        "parts": [{"type": "text", "text": "Order a large Pepperoni"}]
      }
    }
  }'
```

Returns `text/event-stream` with events for `working` → token deltas → `completed`.

### `POST /ag-ui`

AG-UI protocol endpoint for frontend integration. Accepts a message payload and returns an SSE stream.

```bash
curl -X POST http://localhost:8000/ag-ui \
  -H "Content-Type: application/json" \
  -d '{
    "thread_id": "abc-123",
    "run_id": "run-456",
    "messages": [
      {"id": "msg-1", "role": "user", "content": "Show me the menu"}
    ]
  }'
```

Returns `text/event-stream` with AG-UI protocol events (`RUN_STARTED`, `TEXT_MESSAGE_CONTENT`, `TOOL_CALL_START`, etc.).

## Pizza Menu & Tools

### Menu

| Pizza | Price | Description | Prep Time |
|-------|-------|-------------|-----------|
| Margherita | $12.99 | Classic tomato sauce, fresh mozzarella, basil | ~15 min |
| Pepperoni | $14.99 | Pepperoni, mozzarella, tomato sauce | ~15 min |
| BBQ Chicken | $16.99 | BBQ sauce, grilled chicken, red onions, cilantro | ~18 min |
| Veggie Supreme | $15.99 | Bell peppers, mushrooms, olives, onions, tomatoes | ~20 min |
| Hawaiian | $14.99 | Ham, pineapple, mozzarella | ~15 min |
| Meat Lovers | $18.99 | Pepperoni, sausage, ham, bacon, ground beef | ~20 min |
| Four Cheese | $16.99 | Mozzarella, parmesan, gorgonzola, fontina | ~15 min |
| Buffalo Chicken | $17.99 | Buffalo sauce, grilled chicken, blue cheese, celery | ~18 min |

Sizes: **Small** (0.8x), **Medium** (1.0x), **Large** (1.3x)

### Tools

| Tool | Description |
|------|-------------|
| `get_menu()` | Returns the full pizza menu with prices and descriptions |
| `place_order(pizza_name, quantity, size, special_instructions)` | Places an order and returns confirmation with order ID |
| `track_order(order_id)` | Tracks real-time order status |
| `get_specials()` | Returns today's daily specials and promotions |
| `cancel_order(order_id)` | Cancels an order if not yet in baking stage |

## Configuration Reference

| Variable | Default | Description |
|----------|---------|-------------|
| `AZURE_OPENAI_ENDPOINT` | — | Azure OpenAI resource endpoint |
| `AZURE_OPENAI_CHAT_DEPLOYMENT_NAME` | — | Chat model deployment name |
| `AZURE_OPENAI_API_KEY` | — | API key (or omit for DefaultAzureCredential) |
| `USE_FOUNDRY_AGENT` | `false` | Set `true` to use Foundry hosted agent |
| `AZURE_AI_PROJECT_ENDPOINT` | — | Foundry project endpoint (required if Foundry mode) |
| `A2A_AGENT_HOST` | — | Remote A2A agent host for proxying |
| `HOST` | `0.0.0.0` | Server bind address |
| `PORT` | `8000` | Server port |
| `WORKERS` | `1` | Number of uvicorn workers |

---

## References

- [Microsoft Agent Framework – Get Started](https://learn.microsoft.com/en-us/agent-framework/get-started/your-first-agent?pivots=programming-language-python)
- [A2A Protocol Integration](https://learn.microsoft.com/en-us/agent-framework/integrations/a2a?pivots=programming-language-python)
- [AG-UI Protocol Integration](https://learn.microsoft.com/en-us/agent-framework/integrations/ag-ui/?pivots=programming-language-python)
- [Azure AI Foundry](https://learn.microsoft.com/en-us/azure/ai-studio/)
