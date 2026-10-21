---
title: Microsoft Agent Framework orchestration examples
description: Set up and run six multi-agent patterns with Microsoft Agent Framework and Azure AI Foundry.
---

## Overview

These Python examples use Microsoft Agent Framework with `FoundryChatClient`
and `DefaultAzureCredential` to demonstrate different ways to coordinate agents.
Each script includes a sample prompt that you can edit before running it.

## Orchestration patterns

* [Sequential ticket triage](./sequential_orchestration/automated_support_ticket_triage.py)
  passes a support ticket through a summarizer and then a classifier.
* [Concurrent ticket assessment](./concurrent_orchestration/ticket_assessment.py)
  sends the same ticket to sentiment, category, and priority agents in parallel.
* [Group-chat feature review](./group_chat_orchestration/Cross_functional.py)
  lets product, engineering, design, and security agents discuss a proposal under
  a manager's direction, with a maximum of five rounds.
* [Handoff customer support](./handoff_orchestration/dynamic_customer_support.py)
  routes a conversation between triage, refund, and order-status agents.
  It accepts terminal input when the workflow requests more information;
  an empty answer ends the conversation.
* [Magentic blog drafting](./magentic_orchestration/autonomous_blog_drafting.py)
  uses a manager to coordinate a writer and editor, track progress, and replan.
  It allows up to ten rounds and uses a stall limit of two.
* [Hub-and-spoke investment research](./hub_and_spoke_Pattern/README.md)
  keeps a hub in control while specialist tools provide market analysis and
  risk assessment. The risk specialist consumes the saved market report.

## Prerequisites

* Python 3.10 or newer
* [uv](https://docs.astral.sh/uv/getting-started/installation/) for environment
  and dependency management
* An Azure AI Foundry project with a deployed model that supports tool calling
* An Azure identity authorized to invoke that model
* [Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli) if you use
  the local `az login` authentication flow

## Install dependencies

Run all commands below from the parent `GenAI_to_AgenticAI_Projects` directory.
Create a virtual environment if you do not already have one:

```powershell
uv venv .venv-x64 --python 3.12
```

Install only the dependencies needed for these examples:

```powershell
uv pip install --python .venv-x64\Scripts\python.exe -r .\microsoft_agent_framework\requirements.txt
```

The focused [requirements.txt](./requirements.txt) includes the framework core,
Foundry client, orchestration builders, Azure authentication and error types,
OpenAI error types, and `.env` loading. The parent
[requirements.txt](../requirements.txt) also includes this dependency list
alongside packages for the repository's other projects.

## Configure Azure AI Foundry

Set these variables in your environment or in a `.env` file in
`GenAI_to_AgenticAI_Projects`. The scripts call `load_dotenv()`:

```dotenv
AZURE_AI_PROJECT_ENDPOINT=https://your-resource.services.ai.azure.com/api/projects/your-project
AZURE_AI_MODEL_DEPLOYMENT_NAME=your-tool-capable-model-deployment
```

Use the Foundry project endpoint, not an Azure OpenAI resource endpoint.
The deployment name must match the model deployment in your project.
Do not commit credentials or your `.env` file.

For local Azure CLI authentication:

```powershell
az login
```

`DefaultAzureCredential` can also use other supported credential sources,
such as a managed identity in an Azure-hosted environment.

## Run an example

Choose one command:

```powershell
# Sequential ticket triage
.\.venv-x64\Scripts\python.exe .\microsoft_agent_framework\sequential_orchestration\automated_support_ticket_triage.py

# Concurrent sentiment, category, and priority assessment
.\.venv-x64\Scripts\python.exe .\microsoft_agent_framework\concurrent_orchestration\ticket_assessment.py

# Cross-functional group discussion
.\.venv-x64\Scripts\python.exe .\microsoft_agent_framework\group_chat_orchestration\Cross_functional.py

# Interactive customer-support handoffs
.\.venv-x64\Scripts\python.exe .\microsoft_agent_framework\handoff_orchestration\dynamic_customer_support.py

# Manager-led blog drafting and review
.\.venv-x64\Scripts\python.exe .\microsoft_agent_framework\magentic_orchestration\autonomous_blog_drafting.py

# Hub delegation to market and risk specialists
.\.venv-x64\Scripts\python.exe .\microsoft_agent_framework\hub_and_spoke_Pattern\hub_spoke.py
```

The sequential and concurrent examples print agent messages after completion.
The group-chat, handoff, and Magentic examples display intermediate agent output.
The hub-and-spoke example logs specialist calls and prints a final summary.

> [!WARNING]
> Running an example makes billable model calls. These are educational demos:
> the customer-support agents do not access real orders or issue refunds, and the
> investment agents have no live market-data tools. Investment output is not
> current research or personalized financial advice.

## Offline tests

The hub-and-spoke example includes tests with scripted model responses.
They do not require Azure credentials or make network calls. Install the test
runner separately from the runtime dependencies:

```powershell
uv pip install --python .venv-x64\Scripts\python.exe pytest
.\.venv-x64\Scripts\python.exe -m pytest .\microsoft_agent_framework\hub_and_spoke_Pattern\test_hub_spoke.py -q
```

## Troubleshooting

* For missing imports, install the focused requirements using the same Python
  executable that you use to run the script.
* For authentication failures, run `az login` and confirm that your identity has
  permission to invoke the project's model.
* For endpoint or deployment errors, check both environment variables against
  the project and model deployment in Foundry.
* For tool-calling failures, confirm that the deployment supports tool calls.
  Handoff agent names must remain API-safe because they appear in tool names.

## References

* [Exploring multi-agent workflows with Microsoft Agent Framework](https://techcommunity.microsoft.com/blog/azure-ai-foundry-blog/exploring-multi-agent-workflows-with-microsoft-agent-framework/4542512)
* [Microsoft Agent Framework documentation](https://learn.microsoft.com/agent-framework/)