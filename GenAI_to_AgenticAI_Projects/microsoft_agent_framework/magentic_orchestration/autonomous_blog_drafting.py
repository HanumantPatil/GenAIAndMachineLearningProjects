# This orchestration allows for dynamic collaboration of multiple agents.
# Used when the exact workflow is not known upfront, and for complex open-ended problems.

# There is a task ledger which keeps track of the tasks that need to be done.
# The progress ledger keeps track of the tasks completed and what all was learnt.

# The manager agent does the following:

# Maintains the overall goal
# Creates and updates the task ledger
# Chooses which agent should work next
# Tracks progress in the progress ledger
# Replans when stuck
# Synthesizes the final answer

# Use Case: Autonomous Blog Drafting and Review

# Given a topic, a Magentic manager plans and drives an iterative draft-and-review cycle:
# it directs a writer agent to produce the post, routes the draft to an editor agent for clarity and length feedback,
# loops back for revisions when needed,  and finalizes the post once it meets the quality bar — all without a human specifying the step order.


import os
import asyncio
from typing import cast
from agent_framework import AgentResponseUpdate, Message
from agent_framework.foundry import FoundryChatClient
from agent_framework.orchestrations import MagenticBuilder
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

    writer_agent = chat_client.as_agent(
        name="Writer_Agent",
        instructions="You write clear, engaging blog posts on the requested topic.",
        default_options={"store": False},
    )
    editor_agent = chat_client.as_agent(
        name="Editor_Agent",
        instructions="You review drafts for clarity and length, and suggest concise improvements.",
        default_options={"store": False},
    )

    manager_agent = chat_client.as_agent(
        name="Manager_Agent",
        instructions="You coordinate the writer and editor to produce a polished final blog post.",
        default_options={"store": False},
    )

    workflow = MagenticBuilder(
        participants=[writer_agent, editor_agent],
        manager_agent=manager_agent,
        max_stall_count=2,  # Maximum number of consecutive rounds without progress before replanning
        max_round_count=10,  # Maximum number of rounds before the workflow terminates
        intermediate_output_from="all",
    ).build()

    stream = workflow.run(
        "Write a 300-word blog post explaining why sleep matters for productivity.",
        stream=True,
    )

    last_executor = None

    async for event in stream:
        if event.type in ("intermediate", "output") and isinstance(
            event.data, AgentResponseUpdate
        ):
            executor = event.data.author_name
            if executor != last_executor:
                print(f"\n{'-'*60}\n{executor}:\n")
                last_executor = executor
            print(event.data.text, end="", flush=True)
    result = await stream.get_final_response()
    print(f"\n{'='*60}\nFinal Result:\n({len(result.get_outputs())} output messages).")


if __name__ == "__main__":
    asyncio.run(main())


# python .\microsoft_agent_framework\magentic_orchestration\autonomous_blog_drafting.py
