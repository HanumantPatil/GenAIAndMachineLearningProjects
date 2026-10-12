---
title: LangChain LLM Judge Evaluation
description: Run an LLM-as-judge inventory-agent evaluation with LangSmith
ms.date: 2026-10-12
ms.topic: tutorial
---

## Overview

This example uses one Groq model as the inventory agent and another as a judge
that records correctness scores in LangSmith.

## Setup

Run these commands from this folder:

```powershell
uv venv .venv
uv pip install --python .venv\Scripts\python.exe -r requirements.txt
```

Create a `.env` file:

```dotenv
GROQ_API_KEY=your_groq_api_key
LANGSMITH_API_KEY=your_langsmith_api_key
LANGSMITH_PROJECT=your_langsmith_project
LANGSMITH_TRACING=true
```

## Run

```powershell
.\.venv\Scripts\python.exe func_eval.py
```
