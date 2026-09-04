---
title: LangChain Agent Examples
description: Setup and usage guide for the LangChain agents, evaluations, multimodal examples, and guardrails in this project
author: Hanumant Patil
ms.date: 2026-09-03
ms.topic: tutorial
keywords:
  - LangChain
  - Groq
  - LangSmith
  - agents
  - guardrails
estimated_reading_time: 12
---

## Overview

The `agent_lang_chain` examples progress from a basic tool-calling agent to
multimodal analysis, LangSmith evaluations, and PII guardrails. Each numbered
folder can run independently after the shared environment is configured.

The examples use LangChain's `create_agent` API and Groq-hosted chat models.
Folders 5 through 7 also use LangSmith to create a dataset, execute experiments,
and record evaluation scores.

### Learning path

* `1_first_agent`: News agent with one tool and a fallback data source
* `2_agent_with_tool`: Finance agent with multiple selectable tools
* `3_reasoning_agent`: Prompt-guided reasoning without tools
* `4_multimodal_agent`: Remote and base64-encoded image inputs
* `5_func_eval`: Semantic-similarity functional evaluation
* `6_eval_llm_judge.py`: Model-generated correctness scores
* `7_eval_op_metrics`: Named LangSmith experiments for model comparison
* `8_guardrails`: Sensitive-data masking, redaction, and blocking

## Prerequisites

* Python 3.11 or later
* A Groq API key
* Internet access for model requests and external integrations
* A LangSmith account for folders 5 through 7
* The sample images already stored in `4_multimodal_agent/images`

From the repository root, install the shared dependencies into the existing
Windows virtual environment:

```powershell
uv pip install --python .venv-x64\Scripts\python.exe -r requirements.txt
```

Run examples with the same interpreter to avoid package-resolution differences:

```powershell
.\.venv-x64\Scripts\python.exe .\agent_lang_chain\1_first_agent\basic_agent.py
```

## Environment configuration

Create a `.env` file in the repository root. Do not commit real credentials.

```dotenv
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=your_groq_chat_model
GROQ_VISION_MODEL=your_groq_vision_model
SERPAPI_API_KEY=your_serpapi_key
LANGSMITH_API_KEY=your_langsmith_api_key
LANGSMITH_PROJECT=your_langsmith_project
LANGSMITH_TRACING=true
```

* `GROQ_API_KEY`: Authenticates `ChatGroq` requests in all examples
* `GROQ_MODEL`: Selects the chat model in folders 1 through 5 where the
  source does not hardcode it
* `GROQ_VISION_MODEL`: Selects the local-image model in folder 4
* `SERPAPI_API_KEY`: Authenticates SerpAPI news searches in folder 1
* `LANGSMITH_API_KEY`: Authenticates evaluation operations in folders 5
  through 7
* `LANGSMITH_PROJECT`: Groups traces from folders 5 through 7
* `LANGSMITH_TRACING`: Enables tracing for folders 5 through 7

Folders 6, 7, and 8 select Groq-hosted model names directly in code. They still
require `GROQ_API_KEY`.

> [!CAUTION]
> Never paste a real API key into prompts, source files, screenshots, or Git
> history. Revoke and replace any key that may have been exposed.

## Folder details

### 1. First agent

[`1_first_agent/basic_agent.py`](1_first_agent/basic_agent.py) creates a news
reporter with one `search_news` tool. The tool queries SerpAPI for news from the
past day. If SerpAPI reports an invalid key, the tool falls back to the Google
News RSS feed for the India region.

The agent asks for three recent political articles and prints the final model
message. The RSS helper returns up to five entries so the model can choose the
requested three.

```powershell
.\.venv-x64\Scripts\python.exe .\agent_lang_chain\1_first_agent\basic_agent.py
```

### 2. Agent with tools

[`2_agent_with_tool/agent_with_tools.py`](2_agent_with_tool/agent_with_tools.py)
creates a finance agent with two tools:

* `get_stock_price` retrieves a ticker's current price through `yfinance`
* `get_market_valuation_of_private_company` reads static demonstration values
  for OpenAI, Stripe, and SpaceX

The included request asks for OpenAI's private-company valuation, so the agent
should choose the valuation tool. The static values are examples and should not
be treated as current financial data.

```powershell
.\.venv-x64\Scripts\python.exe .\agent_lang_chain\2_agent_with_tool\agent_with_tools.py
```

### 3. Reasoning agent

[`3_reasoning_agent/reasoning_agent.py`](3_reasoning_agent/reasoning_agent.py)
creates an agent with an empty tool list. Its system prompt asks the model to
show numerical reasoning with plain-text formulas. The sample question estimates
travel time between New Delhi and Mumbai at a cheetah's speed.

This is an LLM reasoning demonstration, not a factual route or physics
calculation. No mapping, distance, or animal-performance tool verifies the
answer.

```powershell
.\.venv-x64\Scripts\python.exe .\agent_lang_chain\3_reasoning_agent\reasoning_agent.py
```

### 4. Multimodal agent

[`4_multimodal_agent/multimodal_agent.py`](4_multimodal_agent/multimodal_agent.py)
passes a remote image URL in the user text and asks the configured `GROQ_MODEL`
to return an animal name. The selected model must understand the supplied image
reference for this example to work as intended.

[`4_multimodal_agent/multimodal_agent_classify.py`](4_multimodal_agent/multimodal_agent_classify.py)
loads three local JPEG files, converts them to base64 data URLs, and sends them
as structured `image_url` content blocks. The prompt restricts classification
to clothing categories and requests a JSON array containing item name, item
code, color, gender, and age category.

```powershell
# Analyze the remote image reference.
.\.venv-x64\Scripts\python.exe .\agent_lang_chain\4_multimodal_agent\multimodal_agent.py

# Classify the three local images.
.\.venv-x64\Scripts\python.exe .\agent_lang_chain\4_multimodal_agent\multimodal_agent_classify.py
```

The classifier resolves images relative to its own script, so it can be launched
from the repository root. Its default model is `qwen/qwen3.8-27b` when
`GROQ_VISION_MODEL` is not set.

### 5. Functional evaluation

Folder 5 separates the system under test from the evaluator:

* [`5_func_eval/inventory_agent.py`](5_func_eval/inventory_agent.py) defines a
  tool-backed inventory assistant and exposes `run_agent`
* [`5_func_eval/utils.py`](5_func_eval/utils.py) embeds two answers with
  `all-MiniLM-L6-v2` and calculates cosine similarity
* [`5_func_eval/func_eval.py`](5_func_eval/func_eval.py) creates or reuses the
  `inventorydata` LangSmith dataset and evaluates every case

The dataset covers in-stock, out-of-stock, unknown-product, and out-of-scope
questions. The `semantic_match` evaluator compares reference and generated
answers, then returns a score clipped to the range from 0 to 1.

```powershell
.\.venv-x64\Scripts\python.exe .\agent_lang_chain\5_func_eval\func_eval.py
```

The first run downloads the sentence-transformer model and creates the LangSmith
dataset if it does not exist. Later runs reuse that dataset.

### 6. LLM-as-judge evaluation

Folder 6 keeps the same inventory task and dataset but changes the scoring
method:

* [`6_eval_llm_judge.py/inventory_agent.py`](6_eval_llm_judge.py/inventory_agent.py)
  runs the inventory agent with `openai/gpt-oss-20b`
* [`6_eval_llm_judge.py/func_eval.py`](6_eval_llm_judge.py/func_eval.py) asks
  `openai/gpt-oss-120b` to compare the question, reference answer, and actual
  answer

The judge must return JSON in the form `{"score": <number>}`. The evaluator
parses that JSON and records the result under the `llm_as_judge` metric.

```powershell
.\.venv-x64\Scripts\python.exe .\agent_lang_chain\6_eval_llm_judge.py\func_eval.py
```

Invalid or decorated JSON from the judge causes parsing to fail because this
example intentionally uses direct `json.loads` without a recovery parser.

### 7. Comparative output metrics

Folder 7 returns to sentence-embedding similarity while changing the inventory
agent to `openai/gpt-oss-120b`:

* [`7_eval_op_metrics/inventory_agent.py`](7_eval_op_metrics/inventory_agent.py)
  defines the agent under test
* [`7_eval_op_metrics/utils.py`](7_eval_op_metrics/utils.py) calculates cosine
  similarity
* [`7_eval_op_metrics/func_eval.py`](7_eval_op_metrics/func_eval.py) records the
  evaluation with the `run with openai` experiment prefix

Using the same dataset and metric with a named experiment makes runs easier to
compare in LangSmith.

```powershell
.\.venv-x64\Scripts\python.exe .\agent_lang_chain\7_eval_op_metrics\func_eval.py
```

### 8. Guardrails

[`8_guardrails/guardrails_1.py`](8_guardrails/guardrails_1.py) demonstrates PII
transformation on customer records returned by a tool:

* Credit card middleware masks Luhn-valid card numbers in tool results
* Email middleware redacts addresses in tool results and final model output

The card values are test data. LangChain's built-in credit-card detector checks
the Luhn checksum, so arbitrary 16-digit values may not be classified as cards.

[`8_guardrails/guardrails_2.py`](8_guardrails/guardrails_2.py) provides an
interactive documentation assistant for three fictional languages. A custom
regular expression detects `sk-` and `sk-proj-` style keys in user input. The
`block` strategy raises `PIIDetectionError` before the model call, and `chat`
prints a safe warning instead of submitting the message.

```powershell
# Mask credit cards and redact email addresses.
.\.venv-x64\Scripts\python.exe .\agent_lang_chain\8_guardrails\guardrails_1.py

# Start the interactive API-key blocking example.
.\.venv-x64\Scripts\python.exe .\agent_lang_chain\8_guardrails\guardrails_2.py
```

Type `quit` or `exit` to close the interactive example.

## Evaluation flow

Folders 5 through 7 use the same high-level pipeline:

1. Create or reuse the `inventorydata` dataset in LangSmith.
2. Pass each example's question to the selected inventory agent.
3. Capture the final answer from the agent state.
4. Compare the answer with the dataset's reference answer.
5. Store the metric and trace in LangSmith.

Folder 5 and folder 7 use semantic similarity. Folder 6 uses another LLM as the
judge. Semantic similarity measures closeness in embedding space, while the LLM
judge can assess meaning more flexibly but introduces model cost and variability.

## Project structure

```text
agent_lang_chain/
|-- 1_first_agent/
|   `-- basic_agent.py
|-- 2_agent_with_tool/
|   `-- agent_with_tools.py
|-- 3_reasoning_agent/
|   `-- reasoning_agent.py
|-- 4_multimodal_agent/
|   |-- images/
|   |-- multimodal_agent.py
|   `-- multimodal_agent_classify.py
|-- 5_func_eval/
|   |-- func_eval.py
|   |-- inventory_agent.py
|   `-- utils.py
|-- 6_eval_llm_judge.py/
|   |-- func_eval.py
|   `-- inventory_agent.py
|-- 7_eval_op_metrics/
|   |-- func_eval.py
|   |-- inventory_agent.py
|   `-- utils.py
|-- 8_guardrails/
|   |-- guardrails_1.py
|   `-- guardrails_2.py
|-- BAK/
|   `-- agentic-ai-langchain-main.zip
`-- README.md
```

The `BAK` archive is retained as a backup and is not imported by the active
examples. Generated `__pycache__` folders are also not part of the application
flow.

## Troubleshooting

### LangChain cannot be imported

Run the script with the interpreter where requirements were installed:

```powershell
.\.venv-x64\Scripts\python.exe -c "import langchain; print(langchain.__version__)"
```

### Groq authentication fails

Confirm that `.env` contains `GROQ_API_KEY` and that the key is active. The
guardrail regex only detects key-shaped text; it does not authenticate keys.

### Credit card data is not masked

The built-in detector requires a 16-digit pattern that passes the Luhn checksum.
Use designated payment-provider test numbers for demonstrations, never real card
data.

### LangSmith evaluation fails

Confirm `LANGSMITH_API_KEY`, network access, and dataset permissions. The scripts
create `inventorydata` only when a dataset with that name does not already exist.

### Image classification fails

Confirm the three JPEG files exist under `4_multimodal_agent/images` and that
the selected Groq model supports image input.
