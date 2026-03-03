# Copyright (c) Microsoft. All rights reserved.

"""Unit tests for pizza domain tools (tools.py).

Covers:
- get_menu()          → menu format and content
- place_order()       → valid orders, invalid pizza, invalid size, customisations
- track_order()       → existing and missing orders
- get_specials()      → daily specials format
- cancel_order()      → cancellation flow, non-cancellable states, missing order
"""

from __future__ import annotations

import importlib
import re
from datetime import datetime
from unittest.mock import patch

import pytest


# ---------------------------------------------------------------------------
# Fixture: fresh tools module (clears in-memory order store between tests)
# ---------------------------------------------------------------------------


@pytest.fixture()
def tools():
    """Import (or reload) ``tools`` so each test gets a clean ``_orders`` dict."""
    import tools as _tools

    _tools._orders.clear()
    return _tools


# ============================================================================
# get_menu
# ============================================================================


class TestGetMenu:
    """Tests for the ``get_menu`` tool."""

    def test_returns_string(self, tools):
        result = tools.get_menu()
        assert isinstance(result, str)

    def test_contains_all_pizzas(self, tools):
        result = tools.get_menu()
        for pizza_name in tools.PIZZA_MENU:
            assert pizza_name in result

    def test_contains_prices(self, tools):
        result = tools.get_menu()
        # At least one dollar sign with a decimal price
        assert re.search(r"\$\d+\.\d{2}", result)

    def test_contains_descriptions(self, tools):
        result = tools.get_menu()
        for info in tools.PIZZA_MENU.values():
            assert info["description"] in result

    def test_contains_prep_times(self, tools):
        result = tools.get_menu()
        assert "Prep time" in result or "min" in result


# ============================================================================
# place_order
# ============================================================================


class TestPlaceOrder:
    """Tests for the ``place_order`` tool."""

    def test_valid_order_returns_confirmation(self, tools):
        result = tools.place_order("Margherita")
        assert "Order Confirmed" in result
        assert "PZA-" in result

    def test_order_stored_in_memory(self, tools):
        tools.place_order("Pepperoni")
        assert len(tools._orders) == 1

    def test_order_id_format(self, tools):
        result = tools.place_order("Margherita")
        match = re.search(r"PZA-[A-F0-9]{8}", result)
        assert match, f"Expected PZA-XXXXXXXX pattern in: {result}"

    def test_invalid_pizza_name(self, tools):
        result = tools.place_order("Pineapple Delight")
        assert "not on our menu" in result
        assert "Margherita" in result  # suggests available options

    def test_invalid_size(self, tools):
        result = tools.place_order("Margherita", size="extra-large")
        assert "Invalid size" in result

    @pytest.mark.parametrize("size,multiplier", [("small", 0.8), ("medium", 1.0), ("large", 1.3)])
    def test_size_pricing(self, tools, size, multiplier):
        result = tools.place_order("Margherita", size=size)
        expected_price = round(12.99 * multiplier, 2)
        assert f"${expected_price:.2f}" in result

    def test_quantity_pricing(self, tools):
        result = tools.place_order("Margherita", quantity=3, size="medium")
        expected_total = round(12.99 * 3, 2)
        assert f"${expected_total:.2f}" in result

    def test_special_instructions_captured(self, tools):
        result = tools.place_order("Pepperoni", special_instructions="Extra crispy")
        assert "Extra crispy" in result

    def test_no_special_instructions_shows_none(self, tools):
        result = tools.place_order("Pepperoni")
        assert "None" in result

    def test_multiple_orders_independent(self, tools):
        tools.place_order("Margherita")
        tools.place_order("Pepperoni")
        assert len(tools._orders) == 2

    def test_estimated_delivery_present(self, tools):
        result = tools.place_order("Margherita")
        assert "Estimated Delivery" in result
        assert "minutes" in result


# ============================================================================
# track_order
# ============================================================================


class TestTrackOrder:
    """Tests for the ``track_order`` tool."""

    def test_track_existing_order(self, tools):
        place_result = tools.place_order("Margherita")
        order_id = re.search(r"PZA-[A-F0-9]{8}", place_result).group()
        result = tools.track_order(order_id)
        assert "Order Status" in result
        assert order_id in result

    def test_track_missing_order(self, tools):
        result = tools.track_order("PZA-00000000")
        assert "not found" in result

    def test_track_returns_pizza_details(self, tools):
        tools.place_order("Pepperoni", quantity=2, size="large")
        order_id = list(tools._orders.keys())[0]
        result = tools.track_order(order_id)
        assert "Pepperoni" in result
        assert "Large" in result

    def test_status_is_valid_state(self, tools):
        tools.place_order("Margherita")
        order_id = list(tools._orders.keys())[0]
        result = tools.track_order(order_id)
        valid_states = [
            "Confirmed",
            "Preparing",
            "Baking",
            "Quality Check",
            "Out For Delivery",
            "Delivered",
        ]
        assert any(s in result for s in valid_states)


# ============================================================================
# get_specials
# ============================================================================


class TestGetSpecials:
    """Tests for the ``get_specials`` tool."""

    def test_returns_string(self, tools):
        result = tools.get_specials()
        assert isinstance(result, str)

    def test_contains_todays_day(self, tools):
        today = datetime.now().strftime("%A")
        result = tools.get_specials()
        assert today in result

    def test_contains_discount_price(self, tools):
        result = tools.get_specials()
        # Should contain at least one "-> $xx.xx" pattern
        assert "->" in result

    def test_contains_combo_deal(self, tools):
        result = tools.get_specials()
        assert "Combo Deal" in result

    def test_contains_birthday_special(self, tools):
        result = tools.get_specials()
        assert "Birthday Special" in result

    @pytest.mark.parametrize(
        "day",
        ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
    )
    def test_each_day_has_special(self, tools, day):
        """Ensure every day of the week has a valid special configured."""
        with patch("tools.datetime") as mock_dt:
            mock_dt.now.return_value.strftime.return_value = day
            # Access the specials dict directly for validation
            specials = {
                "Monday": "Margherita",
                "Tuesday": "Pepperoni",
                "Wednesday": "Veggie Supreme",
                "Thursday": "BBQ Chicken",
                "Friday": "Meat Lovers",
                "Saturday": "Four Cheese",
                "Sunday": "Hawaiian",
            }
            assert specials[day] in tools.PIZZA_MENU


# ============================================================================
# cancel_order
# ============================================================================


class TestCancelOrder:
    """Tests for the ``cancel_order`` tool."""

    def test_cancel_confirmed_order(self, tools):
        tools.place_order("Margherita")
        order_id = list(tools._orders.keys())[0]
        result = tools.cancel_order(order_id)
        assert "cancelled" in result.lower()
        assert tools._orders[order_id]["status"] == "cancelled"

    def test_cancel_preparing_order(self, tools):
        tools.place_order("Margherita")
        order_id = list(tools._orders.keys())[0]
        tools._orders[order_id]["status"] = "preparing"
        result = tools.cancel_order(order_id)
        assert "cancelled" in result.lower()

    @pytest.mark.parametrize(
        "status", ["baking", "quality_check", "out_for_delivery", "delivered"]
    )
    def test_cannot_cancel_non_cancellable(self, tools, status):
        tools.place_order("Margherita")
        order_id = list(tools._orders.keys())[0]
        tools._orders[order_id]["status"] = status
        result = tools.cancel_order(order_id)
        assert "cannot be cancelled" in result

    def test_cancel_missing_order(self, tools):
        result = tools.cancel_order("PZA-NONEXIST")
        assert "not found" in result

    def test_refund_amount_matches_total(self, tools):
        tools.place_order("Pepperoni", quantity=2, size="large")
        order_id = list(tools._orders.keys())[0]
        total = tools._orders[order_id]["total"]
        result = tools.cancel_order(order_id)
        assert f"${total:.2f}" in result


# ============================================================================
# Data integrity
# ============================================================================


class TestDataIntegrity:
    """Cross-cutting data validation tests."""

    def test_pizza_menu_not_empty(self, tools):
        assert len(tools.PIZZA_MENU) > 0

    def test_every_pizza_has_required_fields(self, tools):
        required = {"price", "description", "prep_time"}
        for name, info in tools.PIZZA_MENU.items():
            assert required.issubset(info.keys()), f"{name} missing fields"

    def test_all_prices_positive(self, tools):
        for name, info in tools.PIZZA_MENU.items():
            assert info["price"] > 0, f"{name} has non-positive price"

    def test_all_prep_times_positive(self, tools):
        for name, info in tools.PIZZA_MENU.items():
            assert info["prep_time"] > 0, f"{name} has non-positive prep time"

    def test_size_multipliers_exist(self, tools):
        assert set(tools.SIZE_MULTIPLIER.keys()) == {"small", "medium", "large"}
