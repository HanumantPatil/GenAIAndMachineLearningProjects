---
title: Document Fields Analyzer Lab
description: Discover key-value fields in varied documents with Azure Content Understanding.
author: workshop-instructor
ms.topic: tutorial
---

## Scenario

An operations team receives permits, applications, and forms without knowing each layout in advance. This lab uses `prebuilt-documentFields` to discover common key-value fields before the team decides whether to build a custom analyzer.

## About the Analyzer

The Document Fields analyzer finds labels and associated values in varied PDFs
and images without requiring a predefined domain schema. It returns inferred
field names, values, and confidence scores, which makes it useful when document
layouts differ or the desired schema is still being explored.

Use this analyzer for discovery, intake prototypes, and heterogeneous forms.
Unlike the Invoice or US Tax analyzers, its inferred fields are not guaranteed
to follow one stable business schema. Build a custom analyzer when production
automation requires consistent field names and validation rules.

## Scenario Configuration

| Setting | Required value for this lab |
| --- | --- |
| Azure service | Azure Content Understanding in a Microsoft Foundry resource |
| Foundry project | Not required. The analyzer and defaults are configured on the Foundry resource. |
| Analyzer | `prebuilt-documentFields` |
| Example input | `assets/sample-equipment-request.pdf` or `assets/sample-training-request.pdf`, submitted as document bytes |
| Model deployment | Required. Enable automatic deployment in Content Understanding Studio and save the analyzer's supported model mappings as resource defaults. |
| Access | `Cognitive Services User` to configure defaults; API key or `Cognitive Services Content Understanding Reader` to run analysis |
| Verify | Inferred labels, values, and confidence scores for the equipment request fields |

This lab needs no labeling project because it uses a ready-made utility
analyzer. Create a custom analyzer and labeling project only after the desired
production field schema is known.

## Prerequisites

- Python 3.9 or later and an Azure subscription.
- Azure CLI and Bicep CLI when using the Bicep option.
- Configure required model deployments and default mappings in the Microsoft Foundry portal using currently supported versions.

## 1. Create and Configure the Resource

One Microsoft Foundry resource can support all six workshop labs. Use either
the Bicep option or the portal option.

### Option A: Bicep

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
```

### Option B: Azure portal and Content Understanding Studio

1. Sign in to the [Azure portal](https://portal.azure.com/) and create or select
    a resource group in a [supported region](https://learn.microsoft.com/azure/ai-services/content-understanding/language-region-support#region-support).
1. Create a [Microsoft Foundry resource](https://portal.azure.com/#create/Microsoft.CognitiveServicesAIFoundry)
    using the resource group, supported region, a unique name, and **S0** tier.
1. Allow public workshop access, keep local authentication enabled, enable the
    system-assigned managed identity, and complete **Review + create**.
1. Under **Access control (IAM)**, assign **Cognitive Services User** to the
    model configurator and **Cognitive Services Content Understanding Reader**
    to an analysis-only identity.
1. In [Content Understanding Studio settings](https://contentunderstanding.ai.azure.com/settings),
    add the resource, keep automatic deployment of required models enabled, and
    save the configuration.
1. If required, select supported chat and embedding deployments in Microsoft
    Foundry under **Content Understanding Playground** > **Configure**.
1. Copy the endpoint and optional **Key 1** from **Resource Management** >
    **Keys and Endpoint** into `.env`.
1. In Content Understanding Studio, open `prebuilt-documentFields`, run a portal
    sample, and verify the inferred field names, values, and confidence scores.

See the [shared portal guide](../README.md#create-the-services-manually-in-the-portals)
for detailed role, model, and cleanup guidance.

## 2. Install and Run

```powershell
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

## 2A. Test with API-Key Authentication

> [!IMPORTANT]
> Before testing, connect the resource in Content Understanding Studio with
> automatic model deployment enabled. Confirm that supported completion and
> embedding deployments are saved as resource defaults. Without these
> mappings, analysis can finish with no content.

```powershell
python analyze.py $document `
  --output "output/document-fields-test-result.json"
```

The bundled request form contains fictional labels and values. You can replace
its path with another local PDF or image, or with a public HTTPS URL.

A successful test prints inferred fields and confidence scores and creates
`output/document-fields-test-result.json`.

Test the additional employee training request, which uses a different set of
labels and values for schema inference:

```powershell
python analyze.py "assets/sample-training-request.pdf" `
  --output "output/document-fields-training-result.json"
```

## 2B. Test with Microsoft Entra Authentication

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
