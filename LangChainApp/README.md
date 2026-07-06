---
title: LangChainApp
description: LangChain demo application for Azure OpenAI models deployed in Azure AI Foundry.
author: Hanumant Patil
ms.date: 2026-07-06
ms.topic: how-to
keywords:
  - langchain
  - azure openai
  - python
estimated_reading_time: 2
---

## LangChainApp

LangChain demo application for Azure OpenAI models deployed in Azure AI Foundry.

## What Changed

* Added metadata frontmatter
* Kept setup and run instructions aligned with current files

## What It Demonstrates

* Simple chat invocation
* Prompt templates with LCEL chain composition
* Multi-turn conversation history

## Files

* `app.py`: Main demo script
* `requirements.txt`: Python dependencies
* `.env.example`: Environment variable template

## Prerequisites

* Python 3.10+
* Azure OpenAI endpoint and deployment

## Setup

```bash
cd LangChainApp
pip install -r requirements.txt
```

Create a `.env` file (or set environment variables) with:

* `AZURE_OPENAI_ENDPOINT`
* `AZURE_OPENAI_API_KEY`
* `AZURE_OPENAI_DEPLOYMENT_NAME` (optional, defaults to `gpt-4o`)
* `AZURE_OPENAI_API_VERSION` (optional)

## Run

```bash
cd LangChainApp
python app.py
```
