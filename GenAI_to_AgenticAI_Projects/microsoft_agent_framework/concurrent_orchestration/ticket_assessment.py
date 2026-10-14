# In this orchestration, the same input is sent to multiple agents simultaneously and consolidated. Each agent handles tasks independently and the results are combined. All agents work at the same time.
# Used when:

# You need different approaches/perspectives for a problem
# Group decision making-based scenarios
# Voting-based scenarios
# Use Case: Ticket Assessment on Various Criteria

# Consider a customer-support use case in which a new ticket must be assessed quickly and routed correctly. With concurrent orchestration, the same incoming ticket is sent to three specialized agents at the same time.
import os
import asyncio
from dotenv import load_dotenv
from typing import cast
from agent_framework import Message
from azure.identity import DefaultAzureCredential
from agent_framework.foundry import FoundryChatClient
from agent_framework.orchestrations import ConcurrentBuilder

load_dotenv()

async def main() -> None:
    credential = DefaultAzureCredential()

    chat_client = FoundryChatClient(
        project_endpoint=os.getenv("AZURE_AI_PROJECT_ENDPOINT"),
        model=os.getenv("AZURE_AI_MODEL_DEPLOYMENT_NAME"),
        credential=credential,
    )

    sentiment_agent = chat_client.as_agent(
        name="Sentiment Agent",
        instructions="You are a helpful assistant that analyzes the sentiment of a support ticket."
    )

    category_agent = chat_client.as_agent(
        name="Category Agent",
        instructions="You are a helpful assistant that categorizes a support ticket into categories such as Billing, Technical, Refund, or Account."
    )

    priority_agent = chat_client.as_agent(
        name="Priority Agent",
        instructions="You are a helpful assistant that determines the priority of a support ticket as High, Medium, or Low."
    )

    workflow = ConcurrentBuilder(
        participants=[sentiment_agent, category_agent, priority_agent]
    ).build()

    result = await workflow.run(
        "I was charged twice and I'm furious — refund me now!"
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

# python .\microsoft_agent_framework\concurrent_orchestration\ticket_assessment.py