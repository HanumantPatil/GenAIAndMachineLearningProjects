---
title: LangChain Notebook Demos
description: Run the LangChain model, prompt, and output-parser notebooks
ms.date: 2026-10-12
ms.topic: tutorial
---

## Overview

These notebooks demonstrate direct Groq and Ollama calls, prompt templates,
chains, and structured output parsing.

## Setup

Run these commands from this folder:

```powershell
uv venv .venv
uv pip install --python .venv\Scripts\python.exe -r requirements.txt
```

Create a `.env` file when using Groq:

```dotenv
GROQ_API_KEY=your_groq_api_key
```

Ollama examples also require a running local Ollama service and the model named
in the selected notebook.

## Run

```powershell
.\.venv\Scripts\jupyter.exe lab
```
