# Copyright (c) Microsoft. All rights reserved.

"""In-memory pizza order storage.

Provides an :class:`OrderStore` class that encapsulates the order
dictionary, making it easier to test and reason about state.
"""

from __future__ import annotations


class OrderStore:
    """In-memory order store (lightweight, per-worker state)."""

    def __init__(self) -> None:
        self._orders: dict[str, dict] = {}

    # -- dict-like protocol ---------------------------------------------------

    def __contains__(self, order_id: str) -> bool:
        return order_id in self._orders

    def __getitem__(self, order_id: str) -> dict:
        return self._orders[order_id]

    def __setitem__(self, order_id: str, order: dict) -> None:
        self._orders[order_id] = order

    def __len__(self) -> int:
        return len(self._orders)

    # -- convenience ----------------------------------------------------------

    def keys(self):
        """Return a view of all order IDs."""
        return self._orders.keys()

    def clear(self) -> None:
        """Remove all orders (useful for testing)."""
        self._orders.clear()


# Singleton instance shared across all tool functions
order_store = OrderStore()
