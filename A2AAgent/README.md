---
title: Python A2A Agent SDK
description: Reference A2A agent implemented with a2a-sdk, including health checks, agent card discovery, and tests.
author: Hanumant Patil
ms.date: 2026-07-06
ms.topic: how-to
keywords:
  - a2a
  - python
  - agent
  - fastapi
estimated_reading_time: 3
---

## Overview

This folder contains a reference A2A agent implemented with `a2a-sdk`. It includes a sample executor, optional Redis-backed storage, and readiness endpoints.

## What Changed

* Refreshed quick start steps and endpoint references
* Added a clear configuration table and testing flow

## Quick Start

1. Install dependencies

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

2. Run the server

```bash
python main.py
```

* Agent card: `http://localhost:8000/.well-known/agent-card.json`
* Legacy card: `http://localhost:8000/.well-known/agent.json`
* Health: `http://localhost:8000/health`

## Testing

```bash
pytest
```

```bash
python test_agent.py
```

## Configuration

| Variable | Default | Description |
| --- | --- | --- |
| `USE_REDIS` | `false` | Enable Redis-backed task storage and push config |
| `REDIS_HOST` | `localhost` | Redis host |
| `REDIS_PORT` | `6379` | Redis port |
| `REDIS_PASSWORD` | - | Redis password |
| `A2A_HOST` | `0.0.0.0` | Server bind address |
| `A2A_PORT` | `8000` | Server port |

## Extending

Replace `SampleAgentExecutor` in [sample_agent_executor.py](sample_agent_executor.py) with your business logic.
