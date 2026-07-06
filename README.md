---
title: AI Solutions Using Azure AI
description: Multi-solution repository with Azure AI, agentic, and learning-focused projects across Python and .NET
author: Hanumant Patil
ms.date: 2026-07-06
ms.topic: overview
keywords:
  - azure ai
  - agents
  - python
  - dotnet
  - sample projects
estimated_reading_time: 5
---

## Overview

This repository contains Azure AI, agentic, and learning-focused projects across Python and .NET.

## What Changed

* Refreshed solution inventory and grouped projects by purpose.
* Updated setup and run commands for Python and .NET samples.
* Added quick navigation guidance for major folders.

## Repository Structure

| Group | Folders | Purpose |
| --- | --- | --- |
| Agent and protocol samples | `A2AAgent`, `A2AWithAGUI`, `PizzaApp`, `MAF-Demos`, `LangChainApp` | Python samples for A2A, AG-UI, Azure AI Agents, LangChain, and Microsoft Agent Framework workflows |
| Enterprise-style agent solutions | `IT_Helpdesk_MAF_Agents`, `ContosoHRAgent`, `OrchestrateAgent` | Larger projects with layered architecture, UI or API surfaces, and integration-focused workflows |
| .NET learning and algorithms | `CodeApp`, `ONNX` | Console-based C# exercises, design patterns, algorithms, and ML.NET to ONNX export examples |
| Practice and notebooks | `PracticeCode` | Python scripts, notebooks, and small ML or statistics exercises |

## Solution Catalog

| Solution | Tech | Summary |
| --- | --- | --- |
| [A2AAgent](A2AAgent) | Python, FastAPI, A2A SDK | Agent-to-agent protocol service with agent card discovery, streaming support, and tests |
| [A2AWithAGUI](A2AWithAGUI) | Python, FastAPI, Agent Framework | Dual-protocol pizza assistant exposing both A2A and AG-UI endpoints with SSE streaming |
| [PizzaApp](PizzaApp) | Python, Azure AI Agents | Contoso pizza ordering assistant with tools and vector search-backed context |
| [IT_Helpdesk_MAF_Agents](IT_Helpdesk_MAF_Agents) | Python, MAF, Azure AI Search, Cosmos DB | Multi-agent IT helpdesk with RAG, ticketing, escalation, and clean architecture |
| [LangChainApp](LangChainApp) | Python, LangChain, Azure OpenAI | Azure AI Foundry and LangChain examples for chat and prompt chains |
| [MAF-Demos](MAF-Demos) | Python, Microsoft Agent Framework | Workflow demos focused on executors, handlers, edges, and visualization output |
| [ContosoHRAgent](ContosoHRAgent) | .NET, Microsoft Teams, Semantic Kernel | HR-focused agent app with Teams integration and managed identity token flow |
| [OrchestrateAgent](OrchestrateAgent) | .NET, Clean Architecture, Web API | Multi-project .NET solution with API, identity, persistence, and test projects |
| [CodeApp](CodeApp) | .NET | C# practice and algorithm examples |
| [ONNX](ONNX) | .NET, ML.NET, ONNX | ML.NET sample that trains and exports model artifacts to ONNX |
| [PracticeCode](PracticeCode) | Python, NumPy, pandas | Python practice scripts and notebooks for language and data-analysis basics |

## Prerequisites

* Python 3.10+ and `pip` for Python samples
* .NET SDK 8+ for most .NET projects, and .NET 10 for `ContosoHRAgent` and `OrchestrateAgent`
* Azure subscription and Azure AI resources for cloud-integrated samples

## Quick Start

### Python examples

```bash
pip install -r A2AAgent/requirements.txt
python A2AAgent/main.py
```

```bash
pip install -r PizzaApp/requirements.txt
python PizzaApp/agent.py
```

### .NET examples

```bash
dotnet run --project ONNX/ONNX.csproj
```

```bash
dotnet run --project CodeApp/CodeApp.csproj
```

## Notes

* Each solution folder contains its own dependencies and runtime entry points
* Use each project README for environment variables, setup details, and testing instructions
