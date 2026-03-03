# Copyright (c) Microsoft. All rights reserved.

"""Application configuration, constants, and logging setup."""

from __future__ import annotations

import logging
import os

from dotenv import load_dotenv

load_dotenv(override=True)

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

# ---------------------------------------------------------------------------
# Server settings
# ---------------------------------------------------------------------------

HOST: str = os.getenv("HOST", "0.0.0.0")
PORT: int = int(os.getenv("PORT", "8000"))
WORKERS: int = int(os.getenv("WORKERS", "1"))

# Hard-caps in-flight requests to 500 (requirement)
MAX_CONCURRENT_REQUESTS: int = 500

# ---------------------------------------------------------------------------
# Agent mode
# ---------------------------------------------------------------------------

USE_FOUNDRY_AGENT: bool = os.getenv("USE_FOUNDRY_AGENT", "false").lower() == "true"
