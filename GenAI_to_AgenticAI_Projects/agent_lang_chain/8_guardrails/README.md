---
title: LangChain Guardrails
description: Run LangChain PII middleware and redaction examples independently
ms.date: 2026-10-12
ms.topic: tutorial
---

## Overview

These examples demonstrate PII masking, redaction, and blocking around a
Groq-backed LangChain agent.

## Setup

Run these commands from this folder:

```powershell
uv venv .venv
uv pip install --python .venv\Scripts\python.exe -r requirements.txt
```

Create a `.env` file:

```dotenv
GROQ_API_KEY=your_groq_api_key
```

## Run

```powershell
.\.venv\Scripts\python.exe guardrails_1.py
.\.venv\Scripts\python.exe guardrails_2.py
```
