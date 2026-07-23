---
title: GenAI Key Parameters Resources
description: Jupyter notebooks demonstrating key LLM generation parameters — Temperature, Top-p, Top-k, and Output Length — using Hugging Face Transformers and GPT-2.
author: HanumantPatil
ms.date: 2026-07-22
ms.topic: tutorial
keywords:
  - llm parameters
  - temperature
  - top-p
  - top-k
  - output length
  - gpt2
  - hugging face transformers
  - generation config
estimated_reading_time: 4
---

## Overview

This folder contains Jupyter notebooks that explore the core **generation parameters** that control how Large Language Models (LLMs) produce text. All examples use the Hugging Face `transformers` library with the **GPT-2** model.

## Notebooks

| Notebook | Description |
|---|---|
| [`key_params.ipynb`](./key_params.ipynb) | Clean reference notebook — original parameter demonstrations |
| [`key_params_imp.ipynb`](./key_params_imp.ipynb) | Improved notebook — uses `GenerationConfig` to avoid deprecation warnings |

## Key Parameters Explained

### Temperature

Controls the **randomness** of the model output by scaling the logits before sampling.

| Value | Effect |
|---|---|
| `< 1.0` (e.g., `0.1`) | Focused, deterministic, repetitive output |
| `1.0` | Neutral — model's default probability distribution |
| `> 1.0` (e.g., `1.5`) | Creative, diverse, occasionally incoherent output |

```python
generator("Suggest a coffee shop name.", temperature=0.1)   # focused
generator("Suggest a coffee shop name.", temperature=1.5)   # creative
```

### Top-p (Nucleus Sampling)

At each step, only tokens whose **cumulative probability** reaches `p` are considered.

| Value | Effect |
|---|---|
| Low (e.g., `0.2`) | Conservative — picks from a small, high-probability set |
| High (e.g., `0.9`) | Diverse — allows a wide range of tokens |

```python
from transformers import GenerationConfig

gen_config = GenerationConfig(max_new_tokens=3, top_p=0.2, do_sample=True)
generator("The cat sat on", generation_config=gen_config)
```

> **Note:** `do_sample=True` is required when using `top_p`; without it the model uses greedy decoding and ignores `top_p`.

### Top-k

Restricts token selection to the **k most likely** tokens at each step.

| Value | Effect |
|---|---|
| `k=1` | Greedy — always picks the single most likely token |
| `k=20` | Allows broader, more varied outputs |

```python
gen_config = GenerationConfig(max_new_tokens=3, top_k=1, do_sample=True)
generator("The cat sat on", generation_config=gen_config)
```

### Output Length

Controls the **number of tokens** generated.

```python
gen_config = GenerationConfig(max_new_tokens=10)   # generate up to 10 new tokens
generator("The cat sat on", generation_config=gen_config)
```

| Parameter | Description |
|---|---|
| `max_new_tokens` | Maximum number of *new* tokens to generate (excludes prompt) |
| `max_length` | Maximum total sequence length (prompt + generated tokens) |

## Usage Pattern — GenerationConfig (Recommended)

Always use `GenerationConfig` to pass generation parameters to avoid deprecation warnings in recent versions of `transformers`:

```python
from transformers import pipeline, GenerationConfig

generator = pipeline("text-generation", model="gpt2")

gen_config = GenerationConfig(
    max_new_tokens=20,
    temperature=0.7,
    top_p=0.9,
    top_k=50,
    do_sample=True,
)
generator("Once upon a time", generation_config=gen_config)
```

## Related Resources

- [Back to project root](../README.md)
- [Hugging Face GenerationConfig docs](https://huggingface.co/docs/transformers/main_classes/text_generation#transformers.GenerationConfig)
- [GPT-2 model card](https://huggingface.co/gpt2)
