---
title: Document Fields Analyzer Lab
description: Discover key-value fields in varied documents with Azure Content Understanding.
author: workshop-instructor
ms.topic: tutorial
---

## Scenario

An operations team receives permits, applications, and forms without knowing each layout in advance. This lab uses `prebuilt-documentFields` to discover common key-value fields before the team decides whether to build a custom analyzer.

## Prerequisites

- Python 3.9 or later, Azure CLI, Bicep CLI, and an Azure subscription.
- Configure required model deployments and default mappings in the Microsoft Foundry portal using currently supported versions.

## 1. Deploy and Install

To create the shared resource without Bicep, follow the
[manual portal setup](../README.md#create-the-services-manually-in-the-portals),
then return here to install the dependencies.

```powershell
$resourceGroup = "rg-cu-fields-lab"
$location = "eastus"
$accountName = "cu-fields-$((Get-Random -Maximum 99999))"
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
$document = "assets/sample-equipment-request.pdf"
```

Put the endpoint and key in `.env`:

```dotenv
CONTENTUNDERSTANDING_ENDPOINT=https://your-resource.services.ai.azure.com/
CONTENTUNDERSTANDING_KEY=your-api-key
```

## 2A. API-Key Authentication

```powershell
python analyze.py $document --output output/document-fields.json
```

The bundled request form contains fictional labels and values. You can replace
its path with another local PDF or image, or with a public HTTPS URL.

## 2B. Microsoft Entra Authentication

Set `CONTENTUNDERSTANDING_KEY=` in `.env`, then sign in and assign access:

```powershell
az login
$principalId = az ad signed-in-user show --query id --output tsv
$scope = az cognitiveservices account show --resource-group $resourceGroup `
  --name $accountName --query id --output tsv
az role assignment create --assignee-object-id $principalId `
  --assignee-principal-type User --role "Cognitive Services User" --scope $scope
python analyze.py $document
```

## Managed Identity

Assign the Azure compute identity `Cognitive Services Content Understanding Reader`, configure only the endpoint, and leave the key unset.

## Observe

The script prints each discovered field, value, and confidence. Compare this output with the Invoice analyzer: a specialized analyzer provides a stable domain schema, while Document Fields is useful for exploration and varied forms.

## Clean Up

```powershell
az group delete --name $resourceGroup --yes --no-wait
```
