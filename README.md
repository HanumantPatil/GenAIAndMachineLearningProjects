---
title: AI Solutions Using Azure AI
description: Multi-solution repository with Azure AI, agentic, and learning-focused projects across Python and .NET
author: Hanumant Patil
ms.date: 2026-05-12
ms.topic: overview
keywords:
  - azure ai
  - agents
  - python
  - dotnet
  - sample projects
estimated_reading_time: 4
---

## AI Solutions Using Azure AI

This repository contains multiple Azure AI, agentic, and learning-focused solutions across Python and .NET.

## Recently Added Solutions

* [A2AWithAGUI](A2AWithAGUI): Pizza assistant with A2A and AG-UI support, including SSE streaming and a modular FastAPI layout.
* [IT_Helpdesk_MAF_Agents](IT_Helpdesk_MAF_Agents): Multi-agent IT helpdesk with retrieval-augmented context, ticket workflows, and escalation handling.
* [ContosoHRAgent](ContosoHRAgent): Enterprise-focused HR agent solution with Teams integration.

## Solution Catalog

| Solution | Tech | Summary |
| --- | --- | --- |
| [A2AAgent](A2AAgent) | Python, FastAPI, A2A SDK | Agent-to-agent protocol service with agent card discovery, streaming support, and tests. |
| [A2AWithAGUI](A2AWithAGUI) | Python, FastAPI, Agent Framework | Dual-protocol pizza assistant exposing both A2A and AG-UI endpoints with SSE streaming. |
| [PizzaApp](PizzaApp) | Python, Azure AI Agents | Contoso pizza ordering assistant with tools and vector search-backed context. |
| [IT_Helpdesk_MAF_Agents](IT_Helpdesk_MAF_Agents) | Python, MAF, Azure AI Search, Cosmos DB | Multi-agent IT helpdesk with RAG, ticketing, escalation, and clean architecture. |
| [LangChainApp](LangChainApp) | Python, LangChain, Azure OpenAI | Basic Azure AI Foundry + LangChain examples for chat, prompt chains, and multi-turn context. |
| [MAF-Demos](MAF-Demos) | Python, Microsoft Agent Framework | Workflow demos focused on executors, handlers, edges, and visualization output. |
| [ContosoHRAgent](ContosoHRAgent) | .NET, Microsoft Teams, Semantic Kernel | Contoso HR-focused agent app with Teams integration and managed identity token flow. |
| [OrchestrateAgent](OrchestrateAgent) | .NET, Clean Architecture, Web API | Multi-project .NET solution with API, identity, persistence, and test projects. |
| [CodeApp](CodeApp) | .NET | C# practice and algorithm examples (console-based). |
| [ONNX](ONNX) | .NET, ML.NET, ONNX | ML.NET regression training sample that exports model artifacts to ONNX. |
| [PracticeCode](PracticeCode) | Python, NumPy, pandas | Python practice scripts and notebooks for language and data-analysis basics. |

## Prerequisites

* Python 3.10+ and `pip` for Python samples.
* .NET SDK 8+ for current .NET projects.
* Azure subscription and Azure AI resources for cloud-integrated samples.

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
cd ONNX
dotnet run
```

```bash
cd CodeApp
dotnet run
```

## Notes

* Each solution folder contains its own dependencies and entry points.
* See per-solution README files for environment variables, setup details, and testing instructions.
