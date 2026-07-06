---
title: PizzaApp
description: Azure AI Agents sample for a Contoso Pizza ordering assistant with vector search, function tools, and MCP tools.
author: Hanumant Patil
ms.date: 2026-07-06
ms.topic: how-to
keywords:
  - azure ai agents
  - python
  - mcp
  - vector search
estimated_reading_time: 4
---

## PizzaApp

Azure AI Agents sample that powers a Contoso Pizza ordering assistant. It wires together an Azure AI Agent, vector search over store docs, a sizing helper function, and Contoso Pizza MCP APIs.

## What Changed

* Added metadata frontmatter
* Confirmed setup, data upload, and runtime steps

## What it does
- Loads a custom persona from `instructions.txt` to act as Contoso PizzaBot.
- Uses a vector store of Contoso Pizza location docs for store info and hours.
- Calls a function tool (`calculate_pizza_for_people`) for sizing group orders.
- Calls Contoso Pizza MCP microservices for menus, toppings, and orders.
- Runs a simple CLI chat loop so you can converse with the agent.

## Prerequisites
- Python 3.10 or newer.
- Azure subscription with access to Azure AI Foundry (for Agents + vector stores).
- An Azure AI project connection string.

## Environment variables
Create a `.env` file in the `PizzaApp` folder (kept out of git by the root `.gitignore`).

Example `.env`:
```
PROJECT_CONNECTION_STRING=<your-azure-ai-project-endpoint>
# Optional: any Azure auth vars supported by DefaultAzureCredential
# AZURE_TENANT_ID=
# AZURE_CLIENT_ID=
# AZURE_CLIENT_SECRET=
```

## Install dependencies
```bash
python -m venv .venv
. .venv/Scripts/activate  # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Prepare documents and vector store
- Store markdown location files live in `documents/` (sample data is already included).
- To create/upload a vector store from those files, run:
```bash
python add_data.py
```
This uploads files to your Azure AI project, creates a vector store, and prints the new vector store ID and file batch ID. If you use that new ID, update `vector_store_id` inside `agent.py`.

## Run the agent chat loop
```bash
python agent.py
```
- Type messages and press Enter; responses stream back.
- Type `exit` or `quit` to stop.

## Key files
- `agent.py` — builds the toolset (vector search, function tool, MCP tool), creates the agent and thread, and runs the CLI loop with auto function calling and MCP approvals.
- `tools.py` — contains `calculate_pizza_for_people` helper used as a function tool.
- `add_data.py` — uploads docs and builds a vector store.
- `instructions.txt` — persona and behavioral rules for the pizza agent.

## Tips
- Reuse the same vector store across runs to avoid extra uploads; just set the ID in `agent.py`.
- Keep `documents/` updated with store details you want the agent to reference.
- Capture SDK diagnostics when latency or status codes look off; handle 429s with built-in retries from the SDK.
