# Copyright (c) Microsoft. All rights reserved.

"""Unit tests for agent creation and configuration (app.agent.factory).

Covers:
- PIZZA_AGENT_INSTRUCTIONS content
- PIZZA_TOOLS list composition
- PizzaAgentFactory.create_local()   → local mode factory
- PizzaAgentFactory.create_foundry() → Foundry mode factory (async)
"""

from __future__ import annotations

import importlib
import os
from unittest.mock import AsyncMock, MagicMock, patch

import pytest


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _import_factory():
    """Import (or re-import) the ``app.agent.factory`` module."""
    from app.agent import factory as _factory

    return importlib.reload(_factory)


# ============================================================================
# Agent instructions & tools list
# ============================================================================


class TestAgentConfig:
    """Tests for static configuration: instructions and tool list."""

    def test_instructions_contain_agent_name(self):
        factory = _import_factory()
        assert "pizza-agent" in factory.PIZZA_AGENT_INSTRUCTIONS

    def test_instructions_mention_tools(self):
        factory = _import_factory()
        expected = ["get_menu", "place_order", "track_order", "get_specials", "cancel_order"]
        for name in expected:
            assert name in factory.PIZZA_AGENT_INSTRUCTIONS

    def test_instructions_context_aware(self):
        factory = _import_factory()
        assert "context-aware" in factory.PIZZA_AGENT_INSTRUCTIONS.lower()

    def test_instructions_speed_optimized(self):
        factory = _import_factory()
        assert "speed" in factory.PIZZA_AGENT_INSTRUCTIONS.lower()

    def test_pizza_tools_has_five_items(self):
        factory = _import_factory()
        assert len(factory.PIZZA_TOOLS) == 5

    def test_pizza_tools_are_callables(self):
        factory = _import_factory()
        for t in factory.PIZZA_TOOLS:
            assert callable(t)


# ============================================================================
# PizzaAgentFactory.create_local() – Local mode
# ============================================================================


class TestCreatePizzaAgent:
    """Tests for the local-mode agent factory."""

    def test_returns_agent_instance(self):
        factory = _import_factory()
        # AzureOpenAIChatClient is a stub (MagicMock) via conftest
        agent = factory.PizzaAgentFactory.create_local()
        assert agent is not None

    def test_agent_called_with_correct_name(self):
        factory = _import_factory()
        with patch.object(factory, "Agent") as MockAgent:
            factory.PizzaAgentFactory.create_local()
            MockAgent.assert_called_once()
            kwargs = MockAgent.call_args[1]
            assert kwargs["name"] == "pizza-agent"

    def test_agent_receives_instructions(self):
        factory = _import_factory()
        with patch.object(factory, "Agent") as MockAgent:
            factory.PizzaAgentFactory.create_local()
            kwargs = MockAgent.call_args[1]
            assert kwargs["instructions"] == factory.PIZZA_AGENT_INSTRUCTIONS

    def test_agent_receives_tools(self):
        factory = _import_factory()
        with patch.object(factory, "Agent") as MockAgent:
            factory.PizzaAgentFactory.create_local()
            kwargs = MockAgent.call_args[1]
            assert kwargs["tools"] == factory.PIZZA_TOOLS

    def test_agent_receives_client(self):
        factory = _import_factory()
        with patch.object(factory, "Agent") as MockAgent:
            factory.PizzaAgentFactory.create_local()
            kwargs = MockAgent.call_args[1]
            assert kwargs["client"] is not None


# ============================================================================
# PizzaAgentFactory.create_foundry() – Foundry mode
# ============================================================================


class TestCreateFoundryPizzaAgent:
    """Tests for the Foundry-mode agent factory."""

    @pytest.mark.asyncio
    async def test_missing_endpoint_raises(self):
        factory = _import_factory()
        with patch.dict(os.environ, {}, clear=False):
            os.environ.pop("AZURE_AI_PROJECT_ENDPOINT", None)
            with pytest.raises(ValueError, match="AZURE_AI_PROJECT_ENDPOINT"):
                await factory.PizzaAgentFactory.create_foundry()

    @pytest.mark.asyncio
    async def test_returns_tuple_of_three(self):
        import sys
        import types

        factory = _import_factory()

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
                result = await factory.PizzaAgentFactory.create_foundry()
                assert isinstance(result, tuple)
                assert len(result) == 3

    @pytest.mark.asyncio
    async def test_foundry_agent_created_with_correct_name(self):
        import sys
        import types

        factory = _import_factory()

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
                await factory.PizzaAgentFactory.create_foundry()
                mock_provider.create_agent.assert_awaited_once()
                call_kwargs = mock_provider.create_agent.call_args[1]
                assert call_kwargs["name"] == "pizza-agent"
