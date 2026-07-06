---
title: ONNX Sample
description: C# console app using ML.NET to train a regression model and export artifacts to ONNX and ZIP.
author: Hanumant Patil
ms.date: 2026-07-06
ms.topic: how-to
keywords:
  - ml.net
  - onnx
  - dotnet
estimated_reading_time: 2
---

## ONNX Sample

C# console app using ML.NET to train a simple regression model and export it to ONNX and ZIP artifacts.

## What Changed

* Added metadata frontmatter
* Kept build and run instructions aligned with current project layout

## What it does
- Defines a `HealthData` dataset with a single feature `Freq` and label `Factor`.
- Trains an SDCA regression model.
- Runs one prediction for `Freq = 2.5` and prints the result.
- Saves the trained model to `Models/HealthModel.zip` and exports ONNX to `Models/HealthModel.onnx`.

## Prerequisites
- .NET 8 SDK installed.

## Build and run
From the `ONNX` folder:
```bash
dotnet build
dotnet run
```
Outputs printed to console and artifacts written to `Models/`.

## Project file
- `Program.cs` holds all training, prediction, and export code.

## Notes
- Regenerate models any time you change training data or pipeline.
- Check `bin/` and `obj/` for build outputs; these are git-ignored.
