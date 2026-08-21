---
title: OCR Read Analyzer Lab
description: Recognize printed and handwritten text with Azure Content Understanding.
author: workshop-instructor
ms.topic: tutorial
---

## Scenario

A maintenance team receives scanned inspection notes and photographed equipment labels. This lab uses `prebuilt-read` to recognize text while preserving useful page structure in markdown.

The Read analyzer does not require a generative model deployment.

## 1. Deploy and Install

To create the shared resource without Bicep, follow the
[manual portal setup](../README.md#create-the-services-manually-in-the-portals),
then return here to install the dependencies.

```powershell
$resourceGroup = "rg-cu-ocr-lab"
$location = "eastus"
$accountName = "cu-ocr-$((Get-Random -Maximum 99999))"
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
$document = "assets/sample-field-notes.png"
```

Put the endpoint and key in `.env`:

```dotenv
CONTENTUNDERSTANDING_ENDPOINT=https://your-resource.services.ai.azure.com/
CONTENTUNDERSTANDING_KEY=your-api-key
```

## 2A. API-Key Authentication

```powershell
python analyze.py $document --output output/read.json
```

The bundled image contains fictional field notes. You can replace its path with
another local PDF or image, or with a public HTTPS URL.

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

Assign `Cognitive Services Content Understanding Reader` to the Azure compute identity. Configure the endpoint but no key; `DefaultAzureCredential` handles authentication.

## Observe

Compare recognized markdown with the source. Try a clean digital PDF and a skewed phone image, then discuss image quality, handwriting, page coordinates, formulas, and barcodes visible in the full JSON result.

## Clean Up

```powershell
az group delete --name $resourceGroup --yes --no-wait
```
