---
title: First LangChain Agent
description: Run the news-search LangChain agent as an independent example
ms.date: 2026-10-12
ms.topic: tutorial
---

## Overview

This example creates a Groq-backed LangChain agent that searches recent news
with SerpAPI and falls back to Google News RSS when needed.

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
SERPAPI_API_KEY=your_serpapi_key
```

## Run

```powershell
.\.venv\Scripts\python.exe basic_agent.py
```
