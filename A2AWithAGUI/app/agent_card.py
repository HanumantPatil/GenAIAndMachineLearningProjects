# Copyright (c) Microsoft. All rights reserved.

"""A2A Agent Card definition returned by ``/.well-known/agent.json``."""

from __future__ import annotations

from typing import Any

AGENT_CARD: dict[str, Any] = {
    "name": "pizza-agent",
    "description": (
        "AI-powered pizza ordering assistant. "
        "Handles menu browsing, order placement, tracking, specials, and cancellations."
    ),
    "version": "1.0.0",
    "url": "",  # populated dynamically per request
    "capabilities": {
        "streaming": True,
        "pushNotifications": False,
    },
    "skills": [
        {
            "id": "order-pizza",
            "name": "Order Pizza",
            "description": "Place pizza orders with customisation options",
        },
        {
            "id": "track-order",
            "name": "Track Order",
            "description": "Track the status of pizza orders",
        },
        {
            "id": "browse-menu",
            "name": "Browse Menu",
            "description": "View the pizza menu with prices and descriptions",
        },
        {
            "id": "get-specials",
            "name": "Get Specials",
            "description": "Get today's pizza specials and promotions",
        },
    ],
    "defaultInputModes": ["text"],
    "defaultOutputModes": ["text"],
}
