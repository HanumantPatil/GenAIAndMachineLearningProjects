---
title: OrchestrateAgent
description: Multi-project .NET solution with layered architecture, Web API host, and test projects.
author: Hanumant Patil
ms.date: 2026-07-06
ms.topic: overview
keywords:
  - dotnet
  - clean architecture
  - web api
estimated_reading_time: 3
---

## OrchestrateAgent

Multi-project .NET solution following a layered architecture with Web API, identity, persistence, and test projects.

## What Changed

* Added metadata frontmatter
* Confirmed solution build and test commands

## Structure

* `Agents/Agents.sln`: Main solution
* `Agents/Src/Presentation/Agents.WebApi`: API host project (`net10.0`)
* `Agents/Src/Core`: Domain and application layers
* `Agents/Src/Infrastructure`: Identity, persistence, and shared resources
* `Agents/Tests`: Unit, integration, and functional tests

## Prerequisites

* .NET SDK 10.0
* SQL Server (if `UseInMemoryDatabase` is set to `false`)

## Run Web API

```bash
cd OrchestrateAgent/Agents/Src/Presentation/Agents.WebApi
dotnet run
```

## Build Entire Solution

```bash
cd OrchestrateAgent/Agents
dotnet build Agents.sln
```

## Test

```bash
cd OrchestrateAgent/Agents
dotnet test Agents.sln
```
