---
title: LangChain Multimodal Agent
description: Run remote-image and local-image LangChain examples independently
ms.date: 2026-10-12
ms.topic: tutorial
---

## Overview

The folder contains one remote-image example and one local-image classifier.
The local classifier reads the sample files from the `images` folder.

## Setup

Run these commands from this folder:

```powershell
uv venv .venv
uv pip install --python .venv\Scripts\python.exe -r requirements.txt
```

Create a `.env` file:

```dotenv
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=your_multimodal_model
GROQ_VISION_MODEL=your_vision_model
```

## Run

```powershell
.\.venv\Scripts\python.exe multimodal_agent.py
.\.venv\Scripts\python.exe multimodal_agent_classify.py
```
