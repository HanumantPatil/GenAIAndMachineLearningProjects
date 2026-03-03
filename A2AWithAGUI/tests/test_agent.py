# Copyright (c) Microsoft. All rights reserved.

"""Unit tests for agent creation and configuration (agent.py).

Covers:
- PIZZA_AGENT_INSTRUCTIONS content
- PIZZA_TOOLS list composition
- create_pizza_agent()           → local mode factory
- create_foundry_pizza_agent()   → Foundry mode factory (async)
"""

from __future__ import annotations

import importlib
import os
from unittest.mock import AsyncMock, MagicMock, patch

import pytest


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _import_agent():
    """Import (or re-import) the ``agent`` module."""
    import agent as _agent

    return importlib.reload(_agent)


# ============================================================================
# Agent instructions & tools list
# ============================================================================


class TestAgentConfig:
    """Tests for static configuration: instructions and tool list."""

    def test_instructions_contain_agent_name(self):
        agent_mod = _import_agent()
        assert "pizza-agent" in agent_mod.PIZZA_AGENT_INSTRUCTIONS

    def test_instructions_mention_tools(self):
        agent_mod = _import_agent()
        expected = ["get_menu", "place_order", "track_order", "get_specials", "cancel_order"]
        for name in expected:
            assert name in agent_mod.PIZZA_AGENT_INSTRUCTIONS

    def test_instructions_context_aware(self):
        agent_mod = _import_agent()
        assert "context-aware" in agent_mod.PIZZA_AGENT_INSTRUCTIONS.lower()

    def test_instructions_speed_optimized(self):
        agent_mod = _import_agent()
        assert "speed" in agent_mod.PIZZA_AGENT_INSTRUCTIONS.lower()

    def test_pizza_tools_has_five_items(self):
        agent_mod = _import_agent()
        assert len(agent_mod.PIZZA_TOOLS) == 5

    def test_pizza_tools_are_callables(self):
        agent_mod = _import_agent()
        for t in agent_mod.PIZZA_TOOLS:
            assert callable(t)


# ============================================================================
# create_pizza_agent() – Local mode
# ============================================================================


class TestCreatePizzaAgent:
    """Tests for the local-mode agent factory."""

    def test_returns_agent_instance(self):
        agent_mod = _import_agent()
        # AzureOpenAIChatClient is a stub (MagicMock) via conftest
        agent = agent_mod.create_pizza_agent()
        assert agent is not None

    def test_agent_called_with_correct_name(self):
        agent_mod = _import_agent()
        with patch.object(agent_mod, "Agent") as MockAgent:
            agent_mod.create_pizza_agent()
            MockAgent.assert_called_once()
            kwargs = MockAgent.call_args[1]
            assert kwargs["name"] == "pizza-agent"

    def test_agent_receives_instructions(self):
        agent_mod = _import_agent()
        with patch.object(agent_mod, "Agent") as MockAgent:
            agent_mod.create_pizza_agent()
            kwargs = MockAgent.call_args[1]
            assert kwargs["instructions"] == agent_mod.PIZZA_AGENT_INSTRUCTIONS

    def test_agent_receives_tools(self):
        agent_mod = _import_agent()
        with patch.object(agent_mod, "Agent") as MockAgent:
            agent_mod.create_pizza_agent()
            kwargs = MockAgent.call_args[1]
            assert kwargs["tools"] == agent_mod.PIZZA_TOOLS

    def test_agent_receives_client(self):
        agent_mod = _import_agent()
        with patch.object(agent_mod, "Agent") as MockAgent:
            agent_mod.create_pizza_agent()
            kwargs = MockAgent.call_args[1]
            assert kwargs["client"] is not None


# ============================================================================
# create_foundry_pizza_agent() – Foundry mode
# ============================================================================


class TestCreateFoundryPizzaAgent:
    """Tests for the Foundry-mode agent factory."""

    @pytest.mark.asyncio
    async def test_missing_endpoint_raises(self):
        agent_mod = _import_agent()
        with patch.dict(os.environ, {}, clear=False):
            os.environ.pop("AZURE_AI_PROJECT_ENDPOINT", None)
            with pytest.raises(ValueError, match="AZURE_AI_PROJECT_ENDPOINT"):
                await agent_mod.create_foundry_pizza_agent()

    @pytest.mark.asyncio
    async def test_returns_tuple_of_three(self):
        import sys
        import types

        agent_mod = _import_agent()

        mock_provider = MagicMock()
        mock_provider.create_agent = AsyncMock(return_value=MagicMock())

        mock_credential = MagicMock()

        # Stub the lazy-imported modules
        azure_identity_aio = types.ModuleType("azure.identity.aio")
        azure_identity_aio.AzureCliCredential = MagicMock(return_value=mock_credential)

        # Set AzureAIProjectAgentProvider on the existing stub
        sys.modules["agent_framework.azure"].AzureAIProjectAgentProvider = MagicMock(
            return_value=mock_provider
        )

        with patch.dict(os.environ, {"AZURE_AI_PROJECT_ENDPOINT": "https://fake"}):
            with patch.dict(sys.modules, {"azure.identity.aio": azure_identity_aio}):
                result = await agent_mod.create_foundry_pizza_agent()
                assert isinstance(result, tuple)
                assert len(result) == 3

    @pytest.mark.asyncio
    async def test_foundry_agent_created_with_correct_name(self):
        import sys
        import types

        agent_mod = _import_agent()

        mock_provider = MagicMock()
        mock_provider.create_agent = AsyncMock(return_value=MagicMock())

        mock_credential = MagicMock()

        azure_identity_aio = types.ModuleType("azure.identity.aio")
        azure_identity_aio.AzureCliCredential = MagicMock(return_value=mock_credential)

        sys.modules["agent_framework.azure"].AzureAIProjectAgentProvider = MagicMock(
            return_value=mock_provider
        )

        with patch.dict(os.environ, {"AZURE_AI_PROJECT_ENDPOINT": "https://fake"}):
            with patch.dict(sys.modules, {"azure.identity.aio": azure_identity_aio}):
                await agent_mod.create_foundry_pizza_agent()
                mock_provider.create_agent.assert_awaited_once()
                call_kwargs = mock_provider.create_agent.call_args[1]
                assert call_kwargs["name"] == "pizza-agent"
