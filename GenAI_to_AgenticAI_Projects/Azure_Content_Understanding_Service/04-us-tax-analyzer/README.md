---
title: US Tax Analyzer Lab
description: Classify and extract US tax documents with Azure Content Understanding.
author: workshop-instructor
ms.topic: tutorial
---

## Scenario

A tax-intake team receives different US tax forms and needs to classify each form before capturing payer, recipient, income, and withholding fields. This lab uses `prebuilt-tax.us` and displays the detected category, values, and confidence.

Use synthetic or public samples only. Tax forms contain highly sensitive personal and financial data.

## Prerequisites

- Python 3.9 or later, Azure CLI, Bicep CLI, and an Azure subscription.
- Configure required model deployments and default mappings in the Microsoft Foundry portal using currently supported versions.

## 1. Deploy and Install

To create the shared resource without Bicep, follow the
[manual portal setup](../README.md#create-the-services-manually-in-the-portals),
then return here to install the dependencies.

```powershell
$resourceGroup = "rg-cu-tax-lab"
$location = "eastus"
$accountName = "cu-tax-$((Get-Random -Maximum 99999))"
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
$taxForm = "assets/sample-w2.pdf"
```

Put the endpoint and key in `.env`:

```dotenv
CONTENTUNDERSTANDING_ENDPOINT=https://your-resource.services.ai.azure.com/
CONTENTUNDERSTANDING_KEY=your-api-key
```

## 2A. API-Key Authentication

```powershell
python analyze.py $taxForm --output output/tax-form.json
```

The bundled W-2 is clearly marked as fictional training data. You can replace
its path with another synthetic local file or a public HTTPS URL.

## 2B. Microsoft Entra Authentication

Set `CONTENTUNDERSTANDING_KEY=` in `.env`, then sign in and assign access:

```powershell
az login
$principalId = az ad signed-in-user show --query id --output tsv
$scope = az cognitiveservices account show --resource-group $resourceGroup `
  --name $accountName --query id --output tsv
az role assignment create --assignee-object-id $principalId `
  --assignee-principal-type User --role "Cognitive Services User" --scope $scope
python analyze.py $taxForm
```

## Managed Identity

Assign the compute identity `Cognitive Services Content Understanding Reader`, set only the endpoint, and omit the key. `DefaultAzureCredential` selects managed identity in Azure.

## Observe

Check the detected form category before trusting extracted fields. Discuss confidence thresholds, human review, retention, encryption, and why the output is not tax advice.

## Clean Up

```powershell
az group delete --name $resourceGroup --yes --no-wait
```
