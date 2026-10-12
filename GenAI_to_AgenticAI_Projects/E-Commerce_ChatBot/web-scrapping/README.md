---
title: E-Commerce Data Extraction
description: Scrape sample Flipkart product data and load CSV data into SQLite
ms.date: 2026-10-12
ms.topic: tutorial
---

## Overview

The notebook demonstrates browser-based product extraction with Selenium and
Beautiful Soup. The Python script converts a scraped CSV file into SQLite.

## Setup

Run these commands from this folder:

```powershell
uv venv .venv
uv pip install --python .venv\Scripts\python.exe -r requirements.txt
```

## Run

Start the notebook server:

```powershell
.\.venv\Scripts\jupyter.exe lab
```

Convert an exported CSV file:

```powershell
.\.venv\Scripts\python.exe csv_to_sqlite.py
```

Selenium requires an installed Chrome browser. The notebook downloads a
compatible ChromeDriver when necessary.
