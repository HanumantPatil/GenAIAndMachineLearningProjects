# Copyright (c) Microsoft. All rights reserved.

"""Shared pytest fixtures and mock setup for the pizza-agent test suite.

Because the ``agent_framework`` package may not be installed locally,
we inject lightweight stubs into ``sys.modules`` *before* any source
module is imported. Every test module should import the fixture
``mock_agent_framework`` (auto-used) so the stubs are always active.
"""

from __future__ import annotations

import os
import sys
import types
from pathlib import Path
from unittest.mock import MagicMock

import pytest

# ---------------------------------------------------------------------------
# Ensure the project root (parent of tests/) is on sys.path so that
# ``import tools``, ``import agent``, ``import main`` and ``import app``
# all work from tests/.
# ---------------------------------------------------------------------------
_PROJECT_ROOT = str(Path(__file__).resolve().parent.parent)
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)


# ---------------------------------------------------------------------------
# Stub modules for agent_framework & friends
# ---------------------------------------------------------------------------


def _make_stub(name: str) -> types.ModuleType:
    """Create a stub module with a permissive ``__getattr__``."""
    mod = types.ModuleType(name)
    mod.__getattr__ = lambda attr: MagicMock()  # noqa: ARG005
    return mod


_STUBS = {
    "agent_framework": _make_stub("agent_framework"),
    "agent_framework.azure": _make_stub("agent_framework.azure"),
    "agent_framework.ag_ui": _make_stub("agent_framework.ag_ui"),
    "agent_framework.a2a": _make_stub("agent_framework.a2a"),
}


@pytest.fixture(autouse=True)
def mock_agent_framework(monkeypatch):
    """Inject stub modules for ``agent_framework.*`` before each test."""
    for mod_name, stub in _STUBS.items():
        monkeypatch.setitem(sys.modules, mod_name, stub)

    # Provide a real-ish ``@tool`` decorator that is a transparent pass-through
    # so tools functions still behave as plain callables.
    _STUBS["agent_framework"].tool = lambda fn: fn

    yield
