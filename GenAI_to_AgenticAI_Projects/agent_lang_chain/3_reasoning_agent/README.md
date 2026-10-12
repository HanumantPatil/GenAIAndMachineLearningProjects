---
title: LangChain Reasoning Agent
description: Run the prompt-guided reasoning agent independently
ms.date: 2026-10-12
ms.topic: tutorial
---

## Overview

This example uses a Groq-backed LangChain agent to demonstrate prompt-guided
numerical reasoning.

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
.\.venv\Scripts\python.exe reasoning_agent.py
```
