---
title: Groq and Ollama Setup
description: Quick setup steps for Groq and Ollama, with model pull/run commands and a Python chat example
author: Hanumant Patil
ms.date: 2026-07-23
ms.topic: how-to
keywords:
  - groq
  - ollama
  - llm
  - python
estimated_reading_time: 3
---

## Groq setup

1. Sign in to <https://console.groq.com/playground>.
2. Create an API key.
3. Start testing open-source LLMs in the playground.

## Ollama setup

1. Download and install Ollama from <https://ollama.com/>.
2. Pull a model.
3. Run the model locally.

Model page: <https://ollama.com/library/ornith:9b>

## Pull and run the model

```powershell
ollama pull ornith:9b
ollama run ornith:9b
```

## Python example

Python package: <https://github.com/ollama/ollama-python>

```python
from ollama import chat

response = chat(
    model="ornith:9b",
    messages=[{"role": "user", "content": "Hello!"}],
)
print(response.message.content)
```
