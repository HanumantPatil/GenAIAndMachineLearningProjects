---
title: US Tax Analyzer Lab
description: Classify and extract US tax documents with Azure Content Understanding.
author: workshop-instructor
ms.topic: tutorial
---

## Scenario

A tax-intake team receives different US tax forms and needs to classify each form before capturing payer, recipient, income, and withholding fields. This lab uses `prebuilt-tax.us` and displays the detected category, values, and confidence.

Use synthetic or public samples only. Tax forms contain highly sensitive personal and financial data.

## About the Analyzer

The US Tax analyzer identifies supported US tax-document categories and extracts
tax-specific fields. Depending on the detected form, results can include payer,
recipient, wages, income, tax, and withholding values with confidence scores.
The analyzer provides structured extraction, not tax calculations or tax advice.

Use it for tax-document intake and classification when the source forms match
the supported categories. Confirm the detected category and review extracted
values before using them in financial, filing, or compliance workflows.

## Scenario Configuration

| Setting | Required value for this lab |
| --- | --- |
| Azure service | Azure Content Understanding in a Microsoft Foundry resource |
| Foundry project | Not required. The script uses the resource endpoint and analyzer ID. |
| Analyzer | `prebuilt-tax.us` |
| Example input | `assets/sample-w2.pdf` or `assets/sample-w2-second-employee.pdf`, submitted as document bytes |
| Model deployment | Required. Enable automatic deployment in Content Understanding Studio and save the analyzer's supported model mappings as resource defaults. |
| Access | `Cognitive Services User` to configure defaults; API key or `Cognitive Services Content Understanding Reader` to run analysis |
| Verify | W-2 category, payer and recipient values, wages or income, withholding values, and confidence scores |

The analyzer performs classification and extraction only. It does not require a
tax-specific Azure resource, and it does not calculate tax liability. Keep real
tax documents out of the workshop unless approved data-handling controls exist.

## Prerequisites

- Python 3.9 or later and an Azure subscription.
- Azure CLI and Bicep CLI when using the Bicep option.
- Configure required model deployments and default mappings in the Microsoft Foundry portal using currently supported versions.

## 1. Create and Configure the Resource

One Microsoft Foundry resource can support all six workshop labs. Use either
the Bicep option or the portal option.

### Option A: Bicep

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
1. In Content Understanding Studio, open `prebuilt-tax.us`, run a synthetic
    portal sample, and verify the detected form category and extracted fields.

See the [shared portal guide](../README.md#create-the-services-manually-in-the-portals)
for detailed role, model, and cleanup guidance.

## 2. Install and Run

```powershell
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

## 2A. Test with API-Key Authentication

> [!IMPORTANT]
> Before testing, connect the resource in Content Understanding Studio with
> automatic model deployment enabled. Confirm that supported completion and
> embedding deployments are saved as resource defaults. Without these
> mappings, analysis can finish with no content.

```powershell
python analyze.py $taxForm `
  --output "output/us-tax-test-result.json"
```

The bundled W-2 is clearly marked as fictional training data. You can replace
its path with another synthetic local file or a public HTTPS URL.

A successful test prints the detected form category, extracted fields, and
confidence scores and creates `output/us-tax-test-result.json`.

Test the additional fictional W-2 with a second employee and different wage
and withholding values:

```powershell
python analyze.py "assets/sample-w2-second-employee.pdf" `
  --output "output/us-tax-second-employee-result.json"
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
