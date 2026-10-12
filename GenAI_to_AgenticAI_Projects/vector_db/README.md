---
title: Chroma Vector Database Notebooks
description: Run Chroma collection and document lifecycle examples independently
ms.date: 2026-10-12
ms.topic: tutorial
---

## Overview

These notebooks demonstrate Chroma collection creation and document add,
update, query, and delete operations. Local data is stored in the
`news_vectors_db` folder.

## Setup

Run these commands from this folder:

```powershell
uv venv .venv
uv pip install --python .venv\Scripts\python.exe -r requirements.txt
```

## Run

```powershell
.\.venv\Scripts\jupyter.exe lab
```
