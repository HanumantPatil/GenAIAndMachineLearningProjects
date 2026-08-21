---
title: Call Center Analyzer Lab
description: Transcribe support calls and extract customer-service insights with Azure Content Understanding.
author: workshop-instructor
ms.topic: tutorial
---

## Scenario

A support manager wants to review calls for topics, summaries, sentiment, and follow-up actions without listening to every recording. This lab submits an audio or video file to `prebuilt-callCenter` and prints the transcript and structured insights.

Use only recordings that participants are authorized to process. Remove names, account numbers, and other personal data from classroom samples.

## About the Analyzer

The Call Center analyzer processes audio or video conversations. It combines
speech recognition with conversation understanding to produce a transcript and
structured insights such as speaker turns, summaries, sentiment, topics, and
follow-up actions when those values are available for the input.

Use this analyzer to assist support-call review, issue categorization, and
follow-up workflows. Treat sentiment and summaries as decision support. They
must not be the sole basis for employee evaluation or other consequential
decisions.

## Prerequisites

- Python 3.9 or later, Azure CLI, Bicep CLI, and an Azure subscription.
- Configure the domain analyzer's required model deployments and default mappings in the Microsoft Foundry portal using currently supported versions.

## 1. Deploy and Install

To create the shared resource without Bicep, follow the
[manual portal setup](../README.md#create-the-services-manually-in-the-portals),
then return here to install the dependencies.

```powershell
$resourceGroup = "rg-cu-call-lab"
$location = "eastus"
$accountName = "cu-call-$((Get-Random -Maximum 99999))"
az login
az group create --name $resourceGroup --location $location
az deployment group create --resource-group $resourceGroup `
  --template-file infra/main.bicep `
  --parameters accountName=$accountName location=$location
$endpoint = az cognitiveservices account show --resource-group $resourceGroup `
  --name $accountName --query properties.endpoint --output tsv
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env -Force
$recording = "assets/sample-support-call.wav"
```

Put the endpoint and key in `.env`:

```dotenv
CONTENTUNDERSTANDING_ENDPOINT=https://your-resource.services.ai.azure.com/
CONTENTUNDERSTANDING_KEY=your-api-key
```

## 2A. API-Key Authentication

```powershell
python analyze.py $recording --output output/call.json
```

The bundled recording is an offline-synthesized, fictional support call. You can
replace its path with an authorized local recording or a public HTTPS URL.

## 2B. Microsoft Entra Authentication

Set `CONTENTUNDERSTANDING_KEY=` in `.env`, then sign in and assign access:

```powershell
az login
$principalId = az ad signed-in-user show --query id --output tsv
$scope = az cognitiveservices account show --resource-group $resourceGroup `
  --name $accountName --query id --output tsv
az role assignment create --assignee-object-id $principalId `
  --assignee-principal-type User --role "Cognitive Services User" --scope $scope
python analyze.py $recording
```

## Managed Identity

On Azure compute, assign the identity `Cognitive Services Content Understanding Reader`, set the endpoint, and omit the key. The same code uses managed identity through `DefaultAzureCredential`.

## Observe

Compare the transcript with the recording, then inspect returned topics, sentiment, summaries, and actions. Treat these insights as decision support, not an automatic employee-performance score.

## Clean Up

```powershell
az group delete --name $resourceGroup --yes --no-wait
```
