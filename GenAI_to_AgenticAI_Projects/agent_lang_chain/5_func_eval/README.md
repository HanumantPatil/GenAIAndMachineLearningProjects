---
title: LangChain Functional Evaluation
description: Run semantic-similarity evaluations with LangSmith
ms.date: 2026-10-12
ms.topic: tutorial
---

## Overview

This example evaluates an inventory agent with a LangSmith dataset and
sentence-transformer cosine similarity.

## Setup

Run these commands from this folder:

```powershell
uv venv .venv
uv pip install --python .venv\Scripts\python.exe -r requirements.txt
```

Create a `.env` file:

```dotenv
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=your_groq_model
LANGSMITH_API_KEY=your_langsmith_api_key
LANGSMITH_PROJECT=your_langsmith_project
LANGSMITH_TRACING=true
```

## Run

```powershell
.\.venv\Scripts\python.exe func_eval.py
```

The first run downloads the sentence-transformer model and creates the
LangSmith dataset.
