---
title: Foundry Local Examples
description: List, download, and run models with the Foundry Local Python SDK
ms.date: 2026-10-12
ms.topic: tutorial
---

## Overview

`list_models.py` prints aliases from the local model catalog. `app.py`
downloads the required execution providers, loads `qwen2.5-0.5b`, and streams a
sample response.

## Prerequisites

* Python 3.10 or later
* A supported Foundry Local environment
* Internet access for the first model and execution-provider download

## Setup

Run these commands from this folder:

```powershell
uv venv .venv
uv pip install --python .venv\Scripts\python.exe -r requirements.txt
```

On Windows, you can replace `foundry-local-sdk` in `requirements.txt` with
`foundry-local-sdk-winml` to enable Windows ML execution providers.

## Run

```powershell
.\.venv\Scripts\python.exe list_models.py
.\.venv\Scripts\python.exe app.py
```
