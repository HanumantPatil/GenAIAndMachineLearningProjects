# Copyright (c) Microsoft. All rights reserved.

"""Shared runtime state for the pizza-agent server.

Module-level variables that are set during application lifespan
and accessed by route handlers and middleware.
"""

from __future__ import annotations

import asyncio
from typing import Any

from app.config import MAX_CONCURRENT_REQUESTS

# The active pizza-agent instance (set during lifespan startup).
pizza_agent: Any | None = None

# Foundry resources that need async cleanup on shutdown.
foundry_cleanup: list[Any] = []

# Hard-caps in-flight requests to 500 (requirement).
request_semaphore: asyncio.Semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)
