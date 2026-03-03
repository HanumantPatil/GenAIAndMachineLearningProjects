# Copyright (c) Microsoft. All rights reserved.

"""Pizza agent factory – creates local or Foundry-hosted agents.

Contains :class:`PizzaAgentFactory` with two static factory methods,
plus the shared ``PIZZA_AGENT_INSTRUCTIONS`` and ``PIZZA_TOOLS`` list.
"""

from __future__ import annotations

import logging
import os
from typing import Any

from agent_framework import Agent
from agent_framework.azure import AzureOpenAIChatClient

from app.tools.pizza_tools import (
    cancel_order,
    get_menu,
    get_specials,
    place_order,
    track_order,
)

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Agent instructions – context-aware, speed-optimized
# ---------------------------------------------------------------------------

PIZZA_AGENT_INSTRUCTIONS = """\
You are **pizza-agent**, an expert pizza ordering assistant.

Capabilities:
- Browse the pizza menu (get_menu)
- Place orders with size / quantity customisation (place_order)
- Track live order status (track_order)
- Show today's specials & promotions (get_specials)
- Cancel orders before baking starts (cancel_order)

Guidelines:
- Be friendly, concise, and fast.
- Proactively mention today's specials when the customer is browsing.
- Remember customer preferences and earlier context within the conversation
  (you are context-aware).
- Always confirm order details before placing.
- If the customer seems undecided, recommend popular choices.
- Keep responses short to optimise for speed.
"""

PIZZA_TOOLS = [get_menu, place_order, track_order, get_specials, cancel_order]


# ---------------------------------------------------------------------------
# Factory class
# ---------------------------------------------------------------------------


class PizzaAgentFactory:
    """Factory for creating pizza-agent instances.

    Supports two modes:

    1. **Local mode** (default) — ``create_local()`` uses
       ``AzureOpenAIChatClient`` for inference.
       Requires: ``AZURE_OPENAI_ENDPOINT``, ``AZURE_OPENAI_CHAT_DEPLOYMENT_NAME``.

    2. **Foundry mode** — ``create_foundry()`` creates a hosted Foundry agent.
       Requires: ``AZURE_AI_PROJECT_ENDPOINT`` + ``az login``.
       Enable with ``USE_FOUNDRY_AGENT=true`` in ``.env``.
    """

    @staticmethod
    def create_local() -> Agent:
        """Create the pizza-agent using Azure OpenAI (local mode)."""
        client = AzureOpenAIChatClient()

        agent = Agent(
            name="pizza-agent",
            instructions=PIZZA_AGENT_INSTRUCTIONS,
            client=client,
            tools=PIZZA_TOOLS,
        )

        logger.info("pizza-agent created (local mode - AzureOpenAIChatClient)")
        return agent

    @staticmethod
    async def create_foundry() -> tuple[Any, Any, Any]:
        """Create the pizza-agent as a Microsoft Foundry hosted agent.

        Returns:
            ``(agent, credential, provider)`` – caller is responsible
            for closing *credential* and *provider* on shutdown.

        Raises:
            ValueError: If ``AZURE_AI_PROJECT_ENDPOINT`` is not set.
        """
        from azure.identity.aio import AzureCliCredential
        from agent_framework.azure import AzureAIProjectAgentProvider

        endpoint = os.environ.get("AZURE_AI_PROJECT_ENDPOINT")
        if not endpoint:
            raise ValueError(
                "AZURE_AI_PROJECT_ENDPOINT is required for Foundry mode. "
                "Set it in .env or fall back to local mode (USE_FOUNDRY_AGENT=false)."
            )

        credential = AzureCliCredential()
        provider = AzureAIProjectAgentProvider(credential=credential)

        agent = await provider.create_agent(
            name="pizza-agent",
            instructions=PIZZA_AGENT_INSTRUCTIONS,
            tools=PIZZA_TOOLS,
        )

        logger.info("pizza-agent created (Foundry mode - AzureAIProjectAgentProvider)")
        return agent, credential, provider
