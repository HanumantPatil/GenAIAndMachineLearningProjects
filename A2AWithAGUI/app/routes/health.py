# Copyright (c) Microsoft. All rights reserved.

"""Health-check route for operational monitoring."""

from __future__ import annotations

from fastapi import APIRouter

from app.config import MAX_CONCURRENT_REQUESTS

router = APIRouter(tags=["Ops"])


@router.get("/health")
async def health_check():
    """Lightweight health probe."""
    return {
        "status": "healthy",
        "agent": "pizza-agent",
        "protocols": ["ag-ui", "a2a"],
        "streaming": True,
        "max_concurrent_requests": MAX_CONCURRENT_REQUESTS,
    }
