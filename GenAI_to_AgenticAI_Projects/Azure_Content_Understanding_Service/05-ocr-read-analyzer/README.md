---
title: OCR Read Analyzer Lab
description: Recognize printed and handwritten text with Azure Content Understanding.
author: workshop-instructor
ms.topic: tutorial
---

## Scenario

A maintenance team receives scanned inspection notes and photographed equipment labels. This lab uses `prebuilt-read` to recognize text while preserving useful page structure in markdown.

The Read analyzer does not require a generative model deployment.

## About the Analyzer

The OCR Read analyzer recognizes printed and handwritten text in PDFs and
images. It returns readable markdown plus detailed word, line, page, and
location information. Its purpose is text recognition, so it does not infer a
stable business schema or assign semantic meaning to fields.

Use this analyzer to digitize scans, photographs, labels, and notes when the
visible text and its position matter. Choose Layout when document structure such
as sections and tables is central, or choose a domain analyzer when named
business fields are required.

## Scenario Configuration

| Setting | Required value for this lab |
| --- | --- |
| Azure service | Azure Content Understanding in a Microsoft Foundry resource |
| Foundry project | Not required. The script calls the Foundry resource endpoint directly. |
| Analyzer | `prebuilt-read` |
| Example input | `assets/sample-field-notes.png` or `assets/sample-maintenance-log.png`, submitted as image bytes |
| Model deployment | Not required for this content-extraction analyzer |
| Access | API key, or `Cognitive Services Content Understanding Reader` for analysis with Microsoft Entra ID |
| Verify | Printed and handwritten text in markdown, with page, word, line, and location details in JSON |

No separate Vision or Document Intelligence resource is needed for this lab.
Keep the image upright and readable for the baseline run, then vary image
quality to demonstrate OCR limitations.

## Prerequisites

- Python 3.9 or later and an Azure subscription.
- Permission to create Microsoft Cognitive Services resources.
- Azure CLI and Bicep CLI when using the Bicep option.

## 1. Create and Configure the Resource

One Microsoft Foundry resource can support all six workshop labs. Use either
the Bicep option or the portal option.

### Option A: Bicep

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
```

### Option B: Azure portal and Content Understanding Studio

1. Sign in to the [Azure portal](https://portal.azure.com/) and create or select
    a resource group in a [supported region](https://learn.microsoft.com/azure/ai-services/content-understanding/language-region-support#region-support).
1. Create a [Microsoft Foundry resource](https://portal.azure.com/#create/Microsoft.CognitiveServicesAIFoundry)
    using the resource group, supported region, a unique name, and **S0** tier.
1. Allow public workshop access, keep local authentication enabled, enable the
    system-assigned managed identity, and complete **Review + create**.
1. Under **Access control (IAM)**, assign **Cognitive Services User** to the
    person configuring the resource. Assign **Cognitive Services Content
    Understanding Reader** to an analysis-only identity.
1. In [Content Understanding Studio settings](https://contentunderstanding.ai.azure.com/settings),
    add the resource and save it. OCR Read does not require a generative model.
1. Copy the endpoint and optional **Key 1** from **Resource Management** >
    **Keys and Endpoint** into `.env`.
1. In Content Understanding Studio, open `prebuilt-read`, upload an image or
    PDF, and verify the recognized text and markdown output.

See the [shared portal guide](../README.md#create-the-services-manually-in-the-portals)
for detailed role and cleanup guidance.

## 2. Install and Run

```powershell
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

## 2A. Test with API-Key Authentication

```powershell
python analyze.py $document `
  --output "output/ocr-read-test-result.json"
```

The bundled image contains fictional field notes. You can replace its path with
another local PDF or image, or with a public HTTPS URL.

A successful test prints the recognized site-visit notes and creates
`output/ocr-read-test-result.json`. No generative model deployment is required.

Test the additional maintenance shift log, which includes timestamps,
equipment identifiers, measurements, and a follow-up action:

```powershell
python analyze.py "assets/sample-maintenance-log.png" `
  --output "output/ocr-maintenance-log-result.json"
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

Assign `Cognitive Services Content Understanding Reader` to the Azure compute identity. Configure the endpoint but no key; `DefaultAzureCredential` handles authentication.

## Observe

Compare recognized markdown with the source. Try a clean digital PDF and a skewed phone image, then discuss image quality, handwriting, page coordinates, formulas, and barcodes visible in the full JSON result.

## Clean Up

```powershell
az group delete --name $resourceGroup --yes --no-wait
```
