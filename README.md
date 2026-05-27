---
title: AI Solutions Using Azure AI
description: Multi-solution repository with Azure AI, agentic, and learning-focused projects across Python and .NET
author: Hanumant Patil
ms.date: 2026-05-27
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

## Repository Structure

This repository combines production-style agent applications, protocol demos, .NET learning projects, and data-science practice work.

| Group | Folders | Purpose |
| --- | --- | --- |
| Agent and protocol samples | `A2AAgent`, `A2AWithAGUI`, `PizzaApp`, `MAF-Demos`, `LangChainApp` | Python samples for A2A, AG-UI, Azure AI Agents, LangChain, and Microsoft Agent Framework workflows |
| Enterprise-style agent solutions | `IT_Helpdesk_MAF_Agents`, `ContosoHRAgent`, `OrchestrateAgent` | Larger projects with layered architecture, UI or API surfaces, and integration-focused workflows |
| .NET learning and algorithms | `CodeApp`, `ONNX` | Console-based C# exercises, design patterns, algorithms, and ML.NET to ONNX export examples |
| Practice and notebooks | `PracticeCode` | Python scripts, notebooks, and small ML or statistics exercises |

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

## Internal Project Details

| Project | Internal layout highlights | Primary entry point |
| --- | --- | --- |
| [A2AAgent](A2AAgent) | `main.py` hosts the A2A SDK server, `sample_agent_executor.py` contains the sample executor logic, and `tests/` plus `test_agent.py` cover agent behavior and endpoint checks | `python A2AAgent/main.py` |
| [A2AWithAGUI](A2AWithAGUI) | `main.py` exposes FastAPI endpoints, `agent.py` builds the agent, `tools.py` contains pizza tools, and `client_a2a.py` or `client_agui.py` exercise each protocol | `python A2AWithAGUI/main.py` |
| [PizzaApp](PizzaApp) | `agent.py` defines the assistant, `tools.py` holds domain actions, `documents/` contains supporting content, and `instructions.txt` captures assistant guidance | `python PizzaApp/agent.py` |
| [IT_Helpdesk_MAF_Agents](IT_Helpdesk_MAF_Agents) | `src/` follows Clean Architecture with `domain`, `application`, `adapters`, and `infrastructure`; `ui/` contains the Streamlit experience; `data/` stores knowledge-base inputs; `tests/` validates core flows | See the project README for API and UI startup options |
| [ContosoHRAgent](ContosoHRAgent) | `ContosoHRAgent/` contains the ASP.NET Core app, `M365Agent/` contains Microsoft 365 agent assets, and the solution files sit at the project root | `dotnet run --project ContosoHRAgent/ContosoHRAgent` |
| [OrchestrateAgent](OrchestrateAgent) | `Agents/Src/Presentation/Agents.WebApi` hosts the API, `Agents/Src/Core` contains domain and application code, `Agents/Src/Infrastructure` contains shared implementations, and `Agents/Tests` contains automated tests | `dotnet run --project OrchestrateAgent/Agents/Src/Presentation/Agents.WebApi` |
| [CodeApp](CodeApp) | Root-level `.cs` files cover algorithms and design patterns, while subfolders such as `DSA`, `Practice01`, and `SOLID` group practice exercises by topic | `dotnet run --project CodeApp/CodeApp.csproj` |
| [ONNX](ONNX) | `Program.cs` contains the ML.NET training and export flow, and `Models/` stores generated `.zip` and `.onnx` artifacts | `dotnet run --project ONNX/ONNX.csproj` |
| [PracticeCode](PracticeCode) | Mixed Python scripts, CSV datasets, notebooks, and model experiment folders support statistics, NumPy, pandas, and machine-learning practice | Open the target notebook or run the needed script directly |

## Navigation Notes

* Start at the root README when choosing a project, then move to the solution-level README in that folder for setup and environment variables.
* Python projects usually keep their runtime entry points at the folder root and tests in `tests/`.
* Larger .NET solutions use nested solution or source folders, especially in `ContosoHRAgent` and `OrchestrateAgent`.
* Practice-oriented folders such as `CodeApp` and `PracticeCode` are collections of independent examples rather than one deployable application.

## Prerequisites

* Python 3.10+ and `pip` for Python samples.
* .NET SDK 8+ for most .NET projects, with .NET 10 required for `ContosoHRAgent` and `OrchestrateAgent`.
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
