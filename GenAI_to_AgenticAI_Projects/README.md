---
title: GenAI to Agentic AI Projects
description: Hands-on projects exploring Generative AI concepts and progressing towards Agentic AI workflows, using Hugging Face Transformers and GPT-2.
author: HanumantPatil
ms.date: 2026-07-22
ms.topic: overview
keywords:
  - generative ai
  - agentic ai
  - transformers
  - gpt2
  - llm
  - hugging face
estimated_reading_time: 3
---

## Overview

This repository contains hands-on projects that explore core **Generative AI** concepts and progressively build towards **Agentic AI** workflows. Notebooks use the Hugging Face `transformers` library with GPT-2 to demonstrate foundational LLM behaviours.

## Repository Structure

```
GenAI_to_AgenticAI_Projects/
├── GenAI_Key_Parameters_Resources/   # LLM key parameter notebooks
│   ├── key_params.ipynb              # Reference implementation (clean)
│   └── key_params_imp.ipynb          # Improved implementation with GenerationConfig
├── reference_doc.md                  # External reading references
├── requirements.txt                  # Python dependencies
└── README.md                         # This file
```

## Topics Covered

| Topic | Description |
|---|---|
| **Temperature** | Controls output randomness — low values produce focused text, high values produce creative text |
| **Top-p (Nucleus Sampling)** | Limits token selection to the smallest set whose cumulative probability exceeds `p` |
| **Top-k** | Restricts token selection to the top `k` most likely tokens |
| **Output Length** | Controls how many tokens the model generates via `max_new_tokens` / `max_length` |

## Getting Started

### Prerequisites

- Python 3.9 or later
- A virtual environment (`.venv-x64` is used in this project)

### Setup

```powershell
# Activate the virtual environment
.venv-x64\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### Dependencies

```
transformers
torch
datasets
accelerate
sentencepiece
```

## References

- [Building Effective Agents — Anthropic](https://www.anthropic.com/engineering/building-effective-agents)
- [Hugging Face Transformers Documentation](https://huggingface.co/docs/transformers)

## Sub-folders

| Folder | Description |
|---|---|
| [GenAI_Key_Parameters_Resources](./GenAI_Key_Parameters_Resources/README.md) | Notebooks demonstrating key LLM generation parameters |
