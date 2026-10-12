---
title: LangChain Agent with Tools
description: Run the finance tool-calling LangChain agent independently
ms.date: 2026-10-12
ms.topic: tutorial
---

## Overview

This example creates a Groq-backed LangChain agent with stock-price and
private-company valuation tools.

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
```

## Run

```powershell
.\.venv\Scripts\python.exe agent_with_tools.py
```
