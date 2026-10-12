---
title: Finance Data Extractor Backup
description: Run the archived finance data extraction application independently
ms.date: 2026-10-12
ms.topic: reference
---

## Overview

This folder preserves an earlier version of the Streamlit finance data
extractor. Use the parent folder for the current example.

## Setup

Run these commands from this folder:

```powershell
uv venv .venv
uv pip install --python .venv\Scripts\python.exe -r requirements.txt
```

Create a `.env` file containing `GROQ_API_KEY`.

## Run

```powershell
.\.venv\Scripts\streamlit.exe run main.py
```
