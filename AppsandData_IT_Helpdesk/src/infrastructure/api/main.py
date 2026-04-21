"""FastAPI application entry point."""
from __future__ import annotations
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.infrastructure.api.routers.chat import router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa: ANN001
    logger.info("IT Helpdesk API starting up…")
    yield
    logger.info("IT Helpdesk API shutting down…")


app = FastAPI(
    title="IT Helpdesk AI Assistant",
    version="1.0.0",
    description="Agentic IT support powered by Azure AI and Microsoft Agent Framework.",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.exception("Unhandled exception: %s", exc)
    return JSONResponse(
        status_code=500,
        content={"detail": "An internal error occurred. Please try again later."},
    )
