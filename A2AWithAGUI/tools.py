# Copyright (c) Microsoft. All rights reserved.

"""Backward-compatible re-exports from the ``app.tools`` package.

All implementation now lives in:
- ``app.tools.menu``         – PIZZA_MENU, SIZE_MULTIPLIER
- ``app.tools.order_store``  – OrderStore class, order_store singleton
- ``app.tools.pizza_tools``  – @tool functions (get_menu, place_order, …)

This wrapper keeps ``import tools`` working for tests and scripts.
"""

from datetime import datetime  # noqa: F401 – patch target in tests

from app.tools.menu import PIZZA_MENU, SIZE_MULTIPLIER
from app.tools.order_store import order_store
from app.tools.pizza_tools import (
    cancel_order,
    get_menu,
    get_specials,
    place_order,
    track_order,
)

# Backward compat – tests reference ``_orders`` dict directly.
_orders = order_store._orders

__all__ = [
    "PIZZA_MENU",
    "SIZE_MULTIPLIER",
    "_orders",
    "cancel_order",
    "get_menu",
    "get_specials",
    "order_store",
    "place_order",
    "track_order",
]
