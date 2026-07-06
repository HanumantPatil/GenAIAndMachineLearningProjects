---
title: MAF-Demos
description: Workflow and orchestration demos using the Microsoft Agent Framework Python SDK.
author: Hanumant Patil
ms.date: 2026-07-06
ms.topic: overview
keywords:
  - microsoft agent framework
  - python
  - workflow
estimated_reading_time: 2
---

## MAF-Demos

Workflow and orchestration demos using the Microsoft Agent Framework Python SDK.

## What Changed

* Added metadata frontmatter
* Confirmed current demo file and output behavior documentation

## Main Example

* `executors_and_edges.py`: Demonstrates executor nodes, handler typing, workflow edges, and output visualization.

## Prerequisites

* Python 3.10+
* Graphviz installed (required for SVG export)

## Setup

```bash
cd MAF-Demos
pip install -r requirements.txt
```

## Run

```bash
cd MAF-Demos
python executors_and_edges.py
```

## Output

* Prints Mermaid workflow definitions to console
* Saves SVG diagrams to `docs/` when Graphviz is available
