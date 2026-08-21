---
title: Document Layout Analyzer Lab
description: Extract text, tables, sections, and document structure with Azure Content Understanding.
author: workshop-instructor
ms.topic: tutorial
---

## Scenario

A loan-processing team receives policy documents and application forms in many PDF layouts. Before building search or automation, the team needs a consistent representation of headings, paragraphs, tables, and page structure.

This lab uses the `prebuilt-layout` analyzer to turn a document into structured markdown and a detailed JSON result.

## About the Analyzer

The Document Layout analyzer identifies the physical and logical structure of a
PDF or image. It recognizes paragraphs, headings, sections, tables, figures,
selection marks, and page-level coordinates, then represents the content as
markdown and detailed JSON. It does not apply an invoice, tax, or other
business-specific schema.

Use this analyzer when downstream systems need faithful document structure for
search indexing, retrieval-augmented generation, chunking, accessibility, or
document reconstruction. Use a domain analyzer instead when you need stable
business fields such as an invoice total or tax withholding amount.

## What You Learn

- Deploy a Microsoft Foundry resource with Bicep.
- Authenticate with an API key for a classroom exercise.
- Authenticate with Microsoft Entra ID or managed identity for production.
- Submit an asynchronous Content Understanding analysis.
- Read markdown output and save the complete result as JSON.

## Prerequisites

- An Azure subscription.
- Python 3.9 or later.
- Azure CLI and Bicep CLI.
- Permission to create Microsoft Cognitive Services resources.
- A Microsoft Foundry resource in a supported Content Understanding region.

The layout analyzer does not require an LLM deployment. Domain-specific analyzers in later labs can require model deployments and default model mappings.

## 1. Deploy the Azure Resource

To create the shared resource without Bicep, follow the
[manual portal setup](../README.md#create-the-services-manually-in-the-portals),
then continue with step 2.

Open PowerShell in this folder and choose unique values:

```powershell
$resourceGroup = "rg-content-understanding-lab"
$location = "eastus"
$accountName = "cu-layout-$((Get-Random -Maximum 99999))"

az login
az group create --name $resourceGroup --location $location
az deployment group create `
  --resource-group $resourceGroup `
  --template-file infra/main.bicep `
  --parameters accountName=$accountName location=$location
```

Read the endpoint from the deployment output:

```powershell
$endpoint = az deployment group show `
  --resource-group $resourceGroup `
  --name main `
  --query properties.outputs.endpoint.value `
  --output tsv
```

## 2. Create the Python Environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Copy the safe template and open `.env` in the editor:

```powershell
Copy-Item .env.example .env -Force
```

For key authentication, set both values:

```dotenv
CONTENTUNDERSTANDING_ENDPOINT=https://your-resource.services.ai.azure.com/
CONTENTUNDERSTANDING_KEY=your-api-key
```

## 3A. Run with Key Authentication

Use key authentication only for learning and short-lived test resources. Do not store the key in source control.

```powershell
python analyze.py "assets/sample-layout-policy.pdf" `
  --output output/layout-result.json
```

The bundled PDF contains fictional policy sections, a table, and a checklist.
You can replace the path with a public `http` or `https` URL.

When `CONTENTUNDERSTANDING_KEY` exists, the code creates an `AzureKeyCredential`.

## 3B. Run with Microsoft Entra ID

Leave the key empty in `.env` so that the code selects `DefaultAzureCredential`:

```dotenv
CONTENTUNDERSTANDING_ENDPOINT=https://your-resource.services.ai.azure.com/
CONTENTUNDERSTANDING_KEY=
```

Sign in locally:

```powershell
az login
```

Assign yourself access. This command uses the broad `Cognitive Services User` role because it supports both analyzer calls and one-time model-default configuration used by later labs:

```powershell
$principalId = az ad signed-in-user show --query id --output tsv
$scope = az cognitiveservices account show `
  --resource-group $resourceGroup `
  --name $accountName `
  --query id `
  --output tsv

az role assignment create `
  --assignee-object-id $principalId `
  --assignee-principal-type User `
  --role "Cognitive Services User" `
  --scope $scope
```

Role assignments can take several minutes to become effective. Then run:

```powershell
python analyze.py "assets/sample-layout-policy.pdf"
```

For least-privilege analysis-only workloads, use the `Cognitive Services Content Understanding Reader` role when it is available in your subscription.

## Managed Identity in Azure

The Python code does not change when it runs in Azure App Service, Azure Functions, Container Apps, or a virtual machine:

1. Enable a system-assigned or user-assigned managed identity on the compute resource.
2. Assign that identity the `Cognitive Services Content Understanding Reader` role on the Foundry resource.
3. Set only `CONTENTUNDERSTANDING_ENDPOINT` in the application settings.
4. Do not set `CONTENTUNDERSTANDING_KEY` or deploy the local `.env` file.

`DefaultAzureCredential` detects the managed identity automatically.

## How the Code Works

1. `create_client` loads `.env` from the script folder and reads the endpoint.
2. If a key is present, it uses `AzureKeyCredential`.
3. Otherwise, it uses `DefaultAzureCredential`.
4. `begin_analyze` starts the long-running analysis with `prebuilt-layout`.
5. `poller.result()` waits for completion.
6. The script prints markdown and optionally saves the complete JSON result.

## Expected Output

The console displays document content as markdown. Depending on the source document, it can contain:

- Headings and paragraphs.
- Tables represented as markdown tables.
- Page and section structure.
- Recognized printed or handwritten text.

Use the JSON file to inspect detailed page, polygon, table, figure, and span information.

## Troubleshooting

| Problem | Resolution |
| --- | --- |
| Endpoint variable is missing | Set `CONTENTUNDERSTANDING_ENDPOINT` to the Foundry endpoint. |
| HTTP 401 | Verify the API key and endpoint belong to the same resource. |
| HTTP 403 | Check the Entra role assignment and wait for RBAC propagation. |
| Input file does not exist | Run the command from this lab folder or provide an absolute path. |
| URL cannot be downloaded | Use a direct HTTPS URL that the Azure service can access. |
| Region is rejected | Deploy to a region allowed by `infra/main.bicep`. |

## Clean Up

Delete the lab resource group when the session is complete:

```powershell
az group delete --name $resourceGroup --yes --no-wait
```
