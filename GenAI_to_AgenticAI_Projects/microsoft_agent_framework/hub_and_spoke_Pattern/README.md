---
title: Hub-and-spoke investment research
description: Run a Foundry hub agent that delegates market analysis and risk assessment.
---

## How it works

[hub_spoke.py](./hub_spoke.py) uses the same `FoundryChatClient` and
`DefaultAzureCredential` setup as the neighboring orchestration examples.

1. The research hub calls `invoke_market_analysis_agent` with an array of asset classes.
2. The market spoke returns its report to the hub.
3. The hub calls `invoke_risk_assessment_agent`, which receives the saved market report.
4. The hub combines both reports into a final summary.

The framework generates function-tool schemas from the typed Python methods.
`Agent.run` handles the tool-call loop, execution, and submission of tool results;
there is no separate Assistants API polling loop. The spokes do not call each other
or take over the user conversation. Risk assessment rejects calls made before
market analysis, and each research request has its own result state.

## Run the example

Use the project's existing Python environment with dependencies from
[requirements.txt](../../requirements.txt). Configure these values in your
environment or the project's existing `.env` file:

```dotenv
AZURE_AI_PROJECT_ENDPOINT=https://your-resource.services.ai.azure.com/api/projects/your-project
AZURE_AI_MODEL_DEPLOYMENT_NAME=your-tool-capable-model-deployment
```

Authenticate with an identity authorized to invoke the project's model.
For local Azure CLI authentication:

```powershell
az login
.\.venv-x64\Scripts\python.exe .\microsoft_agent_framework\hub_and_spoke_Pattern\hub_spoke.py
```

Run these commands from `GenAI_to_AgenticAI_Projects`. Change `RESEARCH_REQUEST`
in the script to try another portfolio research question. The program logs
specialist invocations and prints the hub's summary. Missing configuration exits
with code 2; failed research exits with code 1.

> [!WARNING]
> This example has no live market-data tools. Its output is an educational,
> model-generated illustration, not current investment research or personalized
> financial advice. Running it makes billable model calls.

## Offline tests

The tests use the installed framework with scripted model responses. They do not
require Azure credentials or make network calls.

```powershell
.\.venv-x64\Scripts\python.exe -m pytest .\microsoft_agent_framework\hub_and_spoke_Pattern\test_hub_spoke.py -q
```
