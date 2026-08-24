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

## Scenario Configuration

| Setting | Required value for this lab |
| --- | --- |
| Azure service | Azure Content Understanding in a Microsoft Foundry resource |
| Foundry project | Not required. Model defaults and analyzer calls use the Foundry resource. |
| Analyzer | `prebuilt-invoice` |
| Example input | `assets/sample-invoice.pdf`, submitted as document bytes |
| Model deployment | Required. In Content Understanding Studio, enable automatic deployment and save the supported completion and embedding mappings as resource defaults. |
| Access | `Cognitive Services User` to configure defaults; API key or `Cognitive Services Content Understanding Reader` to run analysis |
| Verify | Vendor and customer data, invoice identifiers, dates, totals, taxes, confidence scores, and nested line items |

Do not hardcode a model version in the workshop. Studio reads the analyzer's
current supported models and configures the resource-level aliases. A separate
Foundry project is optional and is not consumed by `analyze.py`.

## Prerequisites

- Python 3.9 or later and an Azure subscription.
- Azure CLI and Bicep CLI when using the Bicep option.
- Permission to create Microsoft Cognitive Services resources.
- For this domain analyzer, configure the required model deployment and default model mapping in the Microsoft Foundry portal when prompted. Select a currently supported model version.

## 1. Create and Configure the Resource

One Microsoft Foundry resource can support all six workshop labs. Use either
the Bicep option or the portal option.

### Option A: Bicep

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

### Option B: Azure portal and Content Understanding Studio

1. Sign in to the [Azure portal](https://portal.azure.com/) and create or select
    a resource group in a [supported region](https://learn.microsoft.com/azure/ai-services/content-understanding/language-region-support#region-support).
1. Open [Create a Microsoft Foundry resource](https://portal.azure.com/#create/Microsoft.CognitiveServicesAIFoundry).
1. Select the subscription, resource group, supported region, a globally unique
    name, and the **S0** pricing tier.
1. Allow public network access for the workshop, keep local authentication
    enabled, enable the system-assigned managed identity, and create the resource.
1. Under **Access control (IAM)**, assign **Cognitive Services User** to the
    person configuring models. Assign **Cognitive Services Content Understanding
    Reader** to an analysis-only application identity.
1. Open [Content Understanding Studio settings](https://contentunderstanding.ai.azure.com/settings),
    select **+ Add resource**, choose the resource, keep automatic deployment of
    required models enabled, and select **Save**.
1. If automatic deployment is unavailable, open the resource in
    [Microsoft Foundry](https://ai.azure.com/), go to **Build** > **Models** >
    **AI Services** > **Content Understanding Playground** > **Configure**, and
    save supported chat and embedding deployments as defaults.
1. In the Azure portal, open **Resource Management** > **Keys and Endpoint**.
    Copy the endpoint and, for key authentication, **Key 1** into `.env`.
1. In [Content Understanding Studio](https://contentunderstanding.ai.azure.com/),
    open `prebuilt-invoice` and run a portal sample to verify the configuration.

See the [shared portal guide](../README.md#create-the-services-manually-in-the-portals)
for detailed role, model, and cleanup guidance.

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

## 3A. Test with an API Key

> [!IMPORTANT]
> Before testing, connect the resource in Content Understanding Studio with
> automatic model deployment enabled. The resource defaults must map
> `prebuilt-analyzer-completion` and `prebuilt-analyzer-embedding` to supported
> deployments. Without these mappings, analysis can finish with no content.

```powershell
python analyze.py "assets/sample-invoice.pdf" `
  --output "output/invoice-test-result.json"
```

The bundled invoice is fictional. You can replace its path with a public `http`
or `https` URL.

A successful test prints invoice fields and confidence scores and creates
`output/invoice-test-result.json`.

## 3B. Test with Microsoft Entra ID

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
