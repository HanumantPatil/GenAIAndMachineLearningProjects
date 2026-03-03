# Copyright (c) Microsoft. All rights reserved.

"""Backward-compatible re-exports from the ``app.agent`` package.

All implementation now lives in:
- ``app.agent.factory`` – PizzaAgentFactory class, PIZZA_AGENT_INSTRUCTIONS, PIZZA_TOOLS

This wrapper keeps ``import agent`` working for tests and scripts.
"""

from app.agent.factory import (
    PIZZA_AGENT_INSTRUCTIONS,
    PIZZA_TOOLS,
    PizzaAgentFactory,
)

# Re-export factory methods with original names for backward compat.
create_pizza_agent = PizzaAgentFactory.create_local
create_foundry_pizza_agent = PizzaAgentFactory.create_foundry

__all__ = [
    "PIZZA_AGENT_INSTRUCTIONS",
    "PIZZA_TOOLS",
    "PizzaAgentFactory",
    "create_pizza_agent",
    "create_foundry_pizza_agent",
]
