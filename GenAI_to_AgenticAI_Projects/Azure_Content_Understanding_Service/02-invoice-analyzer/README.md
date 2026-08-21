---
title: Invoice Analyzer Lab
description: Extract invoice header values and line items with Azure Content Understanding.
author: workshop-instructor
ms.topic: tutorial
---

## Scenario

An accounts-payable team manually copies supplier names, invoice numbers, dates, totals, taxes, and line items into an ERP system. This lab uses `prebuilt-invoice` to produce structured values that can be validated before posting.

## About the Analyzer

The Invoice analyzer applies a predefined invoice schema to PDFs and images. It
extracts common header fields such as vendor, customer, invoice number, dates,
purchase order, subtotal, tax, and total, together with itemized descriptions,
quantities, prices, and amounts. Returned confidence scores help identify values
that need human verification.

Use this analyzer for accounts-payable capture when a consistent invoice schema
is more useful than raw text or inferred key-value pairs. Validate totals and
low-confidence fields before posting data to a financial system.

## Prerequisites

- Python 3.9 or later, Azure CLI, Bicep CLI, and an Azure subscription.
- Permission to create Microsoft Cognitive Services resources.
- For this domain analyzer, configure the required model deployment and default model mapping in the Microsoft Foundry portal when prompted. Select a currently supported model version.

## 1. Deploy the Resource

To create the shared resource without Bicep, follow the
[manual portal setup](../README.md#create-the-services-manually-in-the-portals),
then continue with the Python environment commands below.

```powershell
$resourceGroup = "rg-cu-invoice-lab"
$location = "eastus"
$accountName = "cu-invoice-$((Get-Random -Maximum 99999))"
az login
az group create --name $resourceGroup --location $location
az deployment group create --resource-group $resourceGroup `
  --template-file infra/main.bicep `
  --parameters accountName=$accountName location=$location
$endpoint = az cognitiveservices account show --resource-group $resourceGroup `
  --name $accountName --query properties.endpoint --output tsv
```

## 2. Install Dependencies

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env -Force
```

Put the endpoint and key in `.env`:

```dotenv
CONTENTUNDERSTANDING_ENDPOINT=https://your-resource.services.ai.azure.com/
CONTENTUNDERSTANDING_KEY=your-api-key
```

## 3A. Run with an API Key

```powershell
python analyze.py "assets/sample-invoice.pdf" `
  --output output/invoice.json
```

The bundled invoice is fictional. You can replace its path with a public `http`
or `https` URL.

## 3B. Run with Microsoft Entra ID

Set `CONTENTUNDERSTANDING_KEY=` in `.env`, then sign in and assign access:

```powershell
az login
$principalId = az ad signed-in-user show --query id --output tsv
$scope = az cognitiveservices account show --resource-group $resourceGroup `
  --name $accountName --query id --output tsv
az role assignment create --assignee-object-id $principalId `
  --assignee-principal-type User --role "Cognitive Services User" --scope $scope
python analyze.py "assets/sample-invoice.pdf"
```

## Managed Identity

Assign the Azure compute identity `Cognitive Services Content Understanding Reader`, set only `CONTENTUNDERSTANDING_ENDPOINT`, and leave the key unset. `DefaultAzureCredential` then uses managed identity automatically.

## Observe

The script prints every returned field and confidence score, including nested line items. Discuss which low-confidence values require human review and why financial totals should always be validated before posting.

## Clean Up

```powershell
az group delete --name $resourceGroup --yes --no-wait
```
