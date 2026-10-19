# Manages a collaborative conversation between multiple agents, optionally involving a human in the
# process (Human-in-the-Loop). There is a central chat manager that decides which agent responds next and
# when to request for human input.
# Used when:

# Scenarios that require debates or group brainstorming.
# Use Case: Cross-Functional Feature Proposal Review

# A product team uses specialist agents to review a feature proposal in one shared discussion.
# Product Agent assesses value, Engineering Agent feasibility, Design Agent usability, and
# Security Agent compliance. A Manager Agent guides the debate and concludes with a recommendation to proceed,
# revise, or reject.

import os
import asyncio
from typing import cast
from agent_framework import AgentResponseUpdate, Message
from agent_framework.foundry import FoundryChatClient
from agent_framework.orchestrations import GroupChatBuilder
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

    product_agent = chat_client.as_agent(
        name="Product Agent",
        instructions="You are a helpful assistant that argues for user value and business priority.",
        default_options={"store": False},
    )  # Turn off server side storage for this agent
    engineering_agent = chat_client.as_agent(
        name="Engineering Agent",
        instructions="You are a helpful assistant that raises engineering feasibility, effort, and technical risks.",
        default_options={"store": False},
    )  # Turn off server side storage for this agent

    design_agent = chat_client.as_agent(
        name="Design Agent",
        instructions="You are a helpful assistant that focuses on UX and usability concerns.",
        default_options={"store": False},
    )  # Turn off server side storage for this agent

    security_agent = chat_client.as_agent(
        name="Security Agent",
        instructions="You are a helpful assistant that flags compliance and data-protection issues.",
        default_options={"store": False},
    )  # Turn off server side storage for this agent

    manager_agent = chat_client.as_agent(
        name="Manager Agent",
        instructions=(
            "You moderate a design-review discussion. Each turn, choose the SINGLE next "
            "participant to speak from: Product Agent, Engineering Agent, Design Agent, "
            "Security Agent. Never select the same participant twice in a row. Once every "
            "perspective has been heard and a clear decision is reached, terminate the "
            "conversation with a short recommendation."
        ),
        default_options={"store": False},
    )  # Turn off server side storage for this agent

    workflow = GroupChatBuilder(
        participants=[
           product_agent, engineering_agent, design_agent, security_agent
        ],
        orchestrator_agent=manager_agent,
        max_rounds=5,
        intermediate_output_from="all",
    ).build()

    stream = await workflow.run(
        "Proposal: add biometric login to the mobile app. should we build it next quarter?",
        stream=True,
    )

    last_executor = None
    async for event in stream:
        if event.type in ("intermediate", "output") and isinstance(
            event.data, AgentResponseUpdate
        ):
            executor = event.data.author_name
            if executor != last_executor:
                print(f"\n{'-' * 60}\n{executor}:\n")
                last_executor = executor
            print(event.data.text, end="", flush=True)

    result = await stream.get_final_response()
    print(f"\n{'=' * 60}\nFinished ({len(result.get_outputs())} output messages).")


if __name__ == "__main__":
    asyncio.run(main())

# python microsoft_agent_framework/group_chat_orchestration/Cross_functional.py