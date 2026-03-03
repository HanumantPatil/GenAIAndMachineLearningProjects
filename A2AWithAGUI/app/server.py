# Copyright (c) Microsoft. All rights reserved.

"""FastAPI application factory and lifecycle management.

Creates the configured FastAPI application with:
- Lifespan-based agent initialisation and cleanup
- CORS middleware
- A2A and AG-UI protocol endpoints
- Health-check endpoint
"""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager

from agent_framework.ag_ui import add_agent_framework_fastapi_endpoint
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import state
from app.agent import PizzaAgentFactory
from app.config import USE_FOUNDRY_AGENT
from app.routes.a2a import router as a2a_router
from app.routes.health import router as health_router

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Application lifespan – agent initialisation & cleanup
# ---------------------------------------------------------------------------


@asynccontextmanager
async def lifespan(application: FastAPI):
    """Initialise the pizza-agent (local *or* Foundry) before accepting traffic."""

    if USE_FOUNDRY_AGENT:
        agent, credential, provider = await PizzaAgentFactory.create_foundry()
        state.pizza_agent = agent
        state.foundry_cleanup.extend([credential, provider])
    else:
        state.pizza_agent = PizzaAgentFactory.create_local()

    # Register the AG-UI endpoint *after* the agent is ready.
    add_agent_framework_fastapi_endpoint(
        app=application,
        agent=state.pizza_agent,
        path="/ag-ui",
    )
    logger.info("AG-UI endpoint registered at POST /ag-ui")

    yield  # ---------- app is running ----------

    # Cleanup Foundry resources if any
    for resource in reversed(state.foundry_cleanup):
        try:
            await resource.close()
        except Exception:
            logger.warning("Failed to close Foundry resource", exc_info=True)

    logger.info("pizza-agent server shut down")


# ---------------------------------------------------------------------------
# FastAPI application
# ---------------------------------------------------------------------------


def create_app() -> FastAPI:
    """Build and return the fully-configured FastAPI application."""
    application = FastAPI(
        title="Pizza Agent",
        description="AI-powered pizza ordering agent supporting AG-UI and A2A protocols",
        version="1.0.0",
        lifespan=lifespan,
    )

    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.include_router(a2a_router)
    application.include_router(health_router)

    return application


# Module-level app instance for ``uvicorn main:app``.
app = create_app()
