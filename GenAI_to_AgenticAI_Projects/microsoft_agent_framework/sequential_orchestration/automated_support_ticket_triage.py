# Used when the output of one agent is consumed by subsequent agents one after another. 
# This pattern is ideal for workflows where each step depends on the previous one.

# Used When:

# There is a multi-step process, where each step relies on the output of the previous one.
# Situations that benefit from iterative refinement, such as drafting, reviewing, and improving content.
# Each stage produces an output and the next output builds upon that output.
# Use Case: Automated Support Ticket Triage

# Consider a customer-support operation that receives large volumes of unstructured tickets and must route each one accurately. In this sequential workflow, a Summarizer Agent first condenses the raw ticket into one or two sentences that capture the customer’s core intent. Its output is then passed to a Classifier Agent, which assigns exactly one category—Billing, Technical, Refund, or Urgent.


import os
import asyncio
from dotenv import load_dotenv
from typing import cast
from agent_framework import Message
from azure.identity import DefaultAzureCredential
from agent_framework.foundry import FoundryChatClient
from agent_framework.orchestrations import SequentialBuilder


load_dotenv()

async def main() -> None:
    credential = DefaultAzureCredential()

    chat_client = FoundryChatClient(
        project_endpoint=os.getenv("AZURE_AI_PROJECT_ENDPOINT"),
        model=os.getenv("AZURE_AI_MODEL_DEPLOYMENT_NAME"),
        credential=credential,
    )

    summarizer_agent = chat_client.as_agent(
        name="Summarizer Agent",
        description="Summarizes a support ticket into 1-2 sentences of core intent.",
        instructions="You are a helpful assistant that summarizes support tickets into concise summaries."
    )

    classifier_agent = chat_client.as_agent(
        name="Classifier Agent",
        description="Classifies a ticket summary into: Billing, Technical, Refund, or Urgent.",
        instructions="You are a helpful assistant that classifies a support ticket summary strictly into one of the following categories: Billing, Technical, Refund, or Urgent."
    )

    workflow = SequentialBuilder(
        participants=[summarizer_agent, classifier_agent],
        output_from = "all"
    ).build()

    ticket= "I was charged twice for my subscription this month and need a refund ASAP."

    result = await workflow.run(
        ticket
    )
    output = result.get_outputs()

    i = 1
    for response in output:
        for msg in cast(list[Message], response.messages):
            name = msg.author_name or ("assistant" if msg.role == "assistant" else "user")
            print(f"{'-' * 60}\n{i:02d} [{name}]\n{msg.text}")
            i += 1

if __name__ == "__main__":
    asyncio.run(main())

# python .\microsoft_agent_framework\sequential_orchestration\automated_support_ticket_triage.py