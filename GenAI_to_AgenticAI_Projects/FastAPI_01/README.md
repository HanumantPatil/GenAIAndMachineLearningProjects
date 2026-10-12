---
title: FastAPI Example
description: Run the minimal FastAPI application independently
ms.date: 2026-10-12
ms.topic: tutorial
---

## Overview

This folder contains a minimal FastAPI application defined in `main.py`.

## Setup

Run these commands from this folder:

```powershell
uv venv .venv
uv pip install --python .venv\Scripts\python.exe -r requirements.txt
```

## Run

```powershell
.\.venv\Scripts\fastapi.exe dev main.py
```

Open the URL shown by FastAPI, normally <http://127.0.0.1:8000>.
