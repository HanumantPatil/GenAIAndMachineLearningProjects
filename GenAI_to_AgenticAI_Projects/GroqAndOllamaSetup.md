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
Llama 3.1 8B Instruct

Very strong general capabilities (chat, reasoning, code help) in a relatively small size.
ollama pull llama3.1:8b-instruct
ollama run llama3.1:8b-instruct

Mistral 7B Instruct (latest v0.3 or similar)

Known to be roughly ~20% faster than comparable Llama models with similar quality on many everyday tasks.

ollama pull mistral:7b-instruct
ollama run mistral:7b-instruct

On low‑end hardware (8–16 GB, CPU‑only), you might also consider:

Phi‑3 Mini / Phi series (Microsoft)

Designed for efficiency; good reasoning for small parameter count, and runs fast on modest hardware.

Gemma 2B–4B

Very lightweight, suitable when you care more about speed and resource usage than peak accuracy.

| Need                            | Best choice (offline Ollama)      | Why                                                                              |
| ------------------------------- | --------------------------------- | -------------------------------------------------------------------------------- |
| One general assistant           | Llama 3.1 8B Instruct             | Strong accuracy, still relatively fast and lightweight.deploybase+1              |
| Max speed on mid‑range CPU      | Mistral 7B Instruct or Phi‑3 Mini | Smaller, optimized; good enough for 70–80% of daily tasks.localaimaster+1youtube |
| Very low RAM / older laptop     | Gemma small (2–4B) or Phi‑2       | Runs in tight memory budgets with acceptable quality.youtubezeroclaws            |
| Highest local quality (big rig) | Llama 3.x 70B, DeepSeek R1, etc.  | Near cloud‑level reasoning, but heavy and slower.deploybase+1                    |


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
