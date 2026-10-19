# This orchestration lets agents assign a task to other agents based on their expertise.
# Used when:

# Multiple agents are involved, but the order of execution is unknown/non-deterministic.
# Use Case: Dynamic Customer Support Routing

# A Triage Agent greets the customer, identifies the issue, and hands the conversation to the right specialist:
# a Refund Agent for refunds and returns, or an Order Status Agent for shipping updates.
# If the customer’s need changes, the specialist hands the conversation back to triage for seamless rerouting.


import os
import asyncio
from typing import cast
from agent_framework import AgentResponseUpdate, Message
from agent_framework.foundry import FoundryChatClient
from agent_framework.orchestrations import HandoffBuilder
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

load_dotenv()


async def main() -> None:
    credential = DefaultAzureCredential()

    chat_client = FoundryChatClient(
        project_endpoint=os.getenv("AZURE_AI_PROJECT_ENDPOINT"),
        model=os.getenv("AZURE_AI_MODEL_DEPLOYMENT_NAME"),
        credential=credential,
    )

    # Handoff tool names include agent names, so use API-safe names without spaces.
    triage_agent = chat_client.as_agent(
        name="Triage_Agent",
        instructions=(
            "Greet the customer and briefly acknowledge their issue in one sentence, "
            "then hand off to the right specialist."
        ),
        default_options={"store": False},
        require_per_service_call_history_persistence=True,
    )

    refund_agent = chat_client.as_agent(
        name="Refund_Agent",
        instructions="You process refunds and returns. Ask for the order number and resolve the request.",
        default_options={"store": False},
        require_per_service_call_history_persistence=True,
    )

    order_status_agent = chat_client.as_agent(
        name="Order_Status_Agent",
        description="Answers questions about order status and shipping.",
        instructions="You answer order status and shipping questions.",
        default_options={"store": False},
        require_per_service_call_history_persistence=True,
    )

    workflow = (
        HandoffBuilder(participants=[triage_agent, refund_agent, order_status_agent])
        .with_start_agent(triage_agent)
        .add_handoff(
            triage_agent, [refund_agent, order_status_agent]
        )  # triage agent can hand off to refund or order status agents
        .add_handoff(
            refund_agent, [triage_agent]
        )  # refund agent can hand off to triage agent only
        .add_handoff(
            order_status_agent, [triage_agent]
        )  # order status agent can hand off to triage agent only
        .build()
    )

    # Interactive loop: rub once,  then answer each request_info until it ends.

    user_message: str | None = (
        "Hi, I was charged twice for order @12345 and want a refund."
    )
    responses: dict | None = None
    last_executor = None

    while True:
        if responses is not None:
            stream = workflow.run(responses=responses, stream=True)
        else:
            stream = workflow.run(user_message, stream=True)

        pending_request_id = None
        async for event in stream:
            if event.type in ("intermediate", "output") and isinstance(
                event.data, AgentResponseUpdate
            ):
                executor = event.data.author_name
                if executor != last_executor:
                    print(f"\n{'-'*60}\n{executor}:\n")
                    last_executor = executor
                print(event.data.text, end="", flush=True)

            elif event.type == "request_info":
                pending_request_id = (
                    event.request_id
                )  # workflow is waiting for the user
        if pending_request_id is None:
            break  # no input requested --> conversation is complete

        user_text = input("\nYou: ")
        if not user_text.strip():
            break  # empty answer terminates the handoff workflow
        responses = {pending_request_id: [Message(role="user", contents=[user_text])]}


if __name__ == "__main__":
    asyncio.run(main())

# python .\microsoft_agent_framework\handoff_orchestration\dynamic_customer_support.py
