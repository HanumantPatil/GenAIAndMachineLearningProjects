---
title: Finance Data Extractor
description: Extract structured finance data with Streamlit and Groq
ms.date: 2026-10-12
ms.topic: tutorial
---

## Overview

This Streamlit application sends finance text to a Groq-backed LangChain
pipeline and displays the parsed structured result.

## Setup

Run these commands from this folder:

```powershell
uv venv .venv
uv pip install --python .venv\Scripts\python.exe -r requirements.txt
```

Create a `.env` file:

```dotenv
GROQ_API_KEY=your_groq_api_key
```

## Run

```powershell
.\.venv\Scripts\streamlit.exe run main.py
```
