---
title: ContosoHRAgent
description: .NET-based Contoso HR agent solution with Teams integration and Microsoft 365 agent assets.
author: Hanumant Patil
ms.date: 2026-07-06
ms.topic: overview
keywords:
  - dotnet
  - teams
  - semantic kernel
estimated_reading_time: 3
---

## ContosoHRAgent

.NET-based Contoso HR agent solution with Teams integration.

## What Changed

* Added frontmatter metadata for consistent documentation style
* Updated run and build commands to use explicit project paths

## Project Layout

* `ContosoHRAgent/`: Main ASP.NET Core app (`net10.0`) with Teams and Semantic Kernel integration.
* `M365Agent/`: Microsoft 365 Agents Toolkit project assets and app package files.
* `ContosoHRAgent.slnx`: Solution file for the main project set.

## Prerequisites

* .NET SDK 10.0
* Azure resources for managed identity and AI integrations (depending on your environment)

## Run

```bash
dotnet run --project ContosoHRAgent/ContosoHRAgent.csproj
```

## Build

```bash
dotnet build ContosoHRAgent/ContosoHRAgent.csproj
```

## Notes

* App settings are in `appsettings.json` and environment-specific variants.
* Teams and managed identity settings should be configured before running in connected environments.
