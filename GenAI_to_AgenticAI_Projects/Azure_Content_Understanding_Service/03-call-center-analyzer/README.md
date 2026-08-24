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

## Scenario Configuration

| Setting | Required value for this lab |
| --- | --- |
| Azure service | Azure Content Understanding in a Microsoft Foundry resource |
| Foundry project | Not required. The analyzer and model defaults belong to the Foundry resource. |
| Analyzer | `prebuilt-callCenter` |
| Example input | `assets/sample-support-call.wav` or `assets/sample-billing-call.wav`, submitted as audio bytes |
| Model deployment | Required. Enable automatic deployment in Content Understanding Studio and save the analyzer's supported model mappings as resource defaults. |
| Access | `Cognitive Services User` to configure defaults; API key or `Cognitive Services Content Understanding Reader` to run analysis |
| Verify | Transcript, speaker-aware conversation content, and available topics, summary, sentiment, and follow-up fields |

The bundled WAV contains a short, fictional support conversation and requires
no Speech resource or storage account. Use a separate Foundry project only when
your organization needs project-level governance for other assets.

## Prerequisites

- Python 3.9 or later and an Azure subscription.
- Azure CLI and Bicep CLI when using the Bicep option.
- Configure the domain analyzer's required model deployments and default mappings in the Microsoft Foundry portal using currently supported versions.

## 1. Create and Configure the Resource

One Microsoft Foundry resource can support all six workshop labs. Use either
the Bicep option or the portal option.

### Option A: Bicep

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
    model configurator and **Cognitive Services Content Understanding Reader**
    to an analysis-only identity.
1. In [Content Understanding Studio settings](https://contentunderstanding.ai.azure.com/settings),
    add the resource, keep automatic deployment of required models enabled, and
    save the configuration.
1. If needed, configure supported chat and embedding defaults from Microsoft
    Foundry under **Content Understanding Playground** > **Configure**.
1. In the Azure portal, copy the endpoint and optional **Key 1** from
    **Resource Management** > **Keys and Endpoint** into `.env`.
1. In Content Understanding Studio, open `prebuilt-callCenter` and run a portal
    audio sample to verify transcription and structured output.

See the [shared portal guide](../README.md#create-the-services-manually-in-the-portals)
for detailed role, model, and cleanup guidance.

## 2. Install and Run

```powershell
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

## 2A. Test with API-Key Authentication

> [!IMPORTANT]
> Before testing, connect the resource in Content Understanding Studio with
> automatic model deployment enabled. Confirm that supported completion and
> embedding deployments are saved as resource defaults. Without these
> mappings, analysis can finish with no content.

```powershell
python analyze.py $recording `
  --output "output/call-center-test-result.json"
```

The bundled recording is an offline-synthesized, fictional support call. You can
replace its path with an authorized local recording or a public HTTPS URL.

A successful test prints the transcript and available call insights and creates
`output/call-center-test-result.json`.

Test the additional fictional billing call about a duplicate delivery fee and
credit request:

```powershell
python analyze.py "assets/sample-billing-call.wav" `
  --output "output/call-center-billing-test-result.json"
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
