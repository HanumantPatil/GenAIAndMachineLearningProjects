# Copyright (c) Microsoft. All rights reserved.

"""Pizza domain tools for the pizza-agent.

Provides menu browsing, order placement, order tracking, specials,
and cancellation capabilities. All tools are context-aware and
optimized for fast response times.
"""

from __future__ import annotations

import random
import uuid
from datetime import datetime

from agent_framework import tool

# ---------------------------------------------------------------------------
# Pizza menu catalog
# ---------------------------------------------------------------------------

PIZZA_MENU: dict[str, dict] = {
    "Margherita": {
        "price": 12.99,
        "description": "Classic tomato sauce, fresh mozzarella, basil",
        "prep_time": 15,
    },
    "Pepperoni": {
        "price": 14.99,
        "description": "Pepperoni, mozzarella, tomato sauce",
        "prep_time": 15,
    },
    "BBQ Chicken": {
        "price": 16.99,
        "description": "BBQ sauce, grilled chicken, red onions, cilantro",
        "prep_time": 18,
    },
    "Veggie Supreme": {
        "price": 15.99,
        "description": "Bell peppers, mushrooms, olives, onions, tomatoes",
        "prep_time": 20,
    },
    "Hawaiian": {
        "price": 14.99,
        "description": "Ham, pineapple, mozzarella",
        "prep_time": 15,
    },
    "Meat Lovers": {
        "price": 18.99,
        "description": "Pepperoni, sausage, ham, bacon, ground beef",
        "prep_time": 20,
    },
    "Four Cheese": {
        "price": 16.99,
        "description": "Mozzarella, parmesan, gorgonzola, fontina",
        "prep_time": 15,
    },
    "Buffalo Chicken": {
        "price": 17.99,
        "description": "Buffalo sauce, grilled chicken, blue cheese, celery",
        "prep_time": 18,
    },
}

# In-memory order store (lightweight, per-worker state)
_orders: dict[str, dict] = {}

SIZE_MULTIPLIER = {"small": 0.8, "medium": 1.0, "large": 1.3}

# ---------------------------------------------------------------------------
# Tools
# ---------------------------------------------------------------------------


@tool
def get_menu() -> str:
    """Get the full pizza menu with prices and descriptions.

    Returns:
        A formatted pizza menu with all available pizzas, prices, and descriptions.
    """
    lines = ["Pizza Menu:", "=" * 40]
    for name, info in PIZZA_MENU.items():
        lines.append(f"  {name}: ${info['price']:.2f}")
        lines.append(f"    {info['description']}")
        lines.append(f"    Prep time: ~{info['prep_time']} min")
        lines.append("")
    return "\n".join(lines)


@tool
def place_order(
    pizza_name: str,
    quantity: int = 1,
    size: str = "medium",
    special_instructions: str = "",
) -> str:
    """Place a pizza order.

    Args:
        pizza_name: Name of the pizza to order (e.g. 'Margherita', 'Pepperoni').
        quantity: Number of pizzas to order (default 1).
        size: Size of the pizza - 'small', 'medium', or 'large' (default 'medium').
        special_instructions: Any special instructions for the order.

    Returns:
        Order confirmation with order ID and estimated delivery time.
    """
    if pizza_name not in PIZZA_MENU:
        available = ", ".join(PIZZA_MENU.keys())
        return f"Sorry, '{pizza_name}' is not on our menu. Available pizzas: {available}"

    if size not in SIZE_MULTIPLIER:
        return f"Invalid size '{size}'. Choose from: small, medium, large"

    pizza = PIZZA_MENU[pizza_name]
    unit_price = pizza["price"] * SIZE_MULTIPLIER[size]
    total = unit_price * quantity

    order_id = f"PZA-{uuid.uuid4().hex[:8].upper()}"
    prep_time = pizza["prep_time"] + 5 * (quantity - 1)
    delivery_time = prep_time + random.randint(15, 25)

    order = {
        "order_id": order_id,
        "pizza": pizza_name,
        "size": size,
        "quantity": quantity,
        "unit_price": round(unit_price, 2),
        "total": round(total, 2),
        "special_instructions": special_instructions,
        "status": "confirmed",
        "placed_at": datetime.now().isoformat(),
        "estimated_delivery_minutes": delivery_time,
    }
    _orders[order_id] = order

    return (
        f"Order Confirmed!\n"
        f"Order ID: {order_id}\n"
        f"Pizza: {quantity}x {size.capitalize()} {pizza_name}\n"
        f"Total: ${total:.2f}\n"
        f"Special Instructions: {special_instructions or 'None'}\n"
        f"Estimated Delivery: ~{delivery_time} minutes"
    )


@tool
def track_order(order_id: str) -> str:
    """Track the status of a pizza order.

    Args:
        order_id: The order ID to track (e.g. 'PZA-ABCD1234').

    Returns:
        Current order status and details.
    """
    if order_id not in _orders:
        return f"Order '{order_id}' not found. Please check your order ID."

    order = _orders[order_id]
    statuses = [
        "confirmed",
        "preparing",
        "baking",
        "quality_check",
        "out_for_delivery",
        "delivered",
    ]
    # Simulate progress
    current_idx = min(random.randint(0, len(statuses) - 1), len(statuses) - 1)
    order["status"] = statuses[current_idx]

    return (
        f"Order Status: {order['status'].replace('_', ' ').title()}\n"
        f"Order ID: {order['order_id']}\n"
        f"Pizza: {order['quantity']}x {order['size'].capitalize()} {order['pizza']}\n"
        f"Placed: {order['placed_at']}\n"
        f"Estimated Delivery: ~{order['estimated_delivery_minutes']} minutes"
    )


@tool
def get_specials() -> str:
    """Get today's pizza specials and promotions.

    Returns:
        Current special offers and promotions.
    """
    day = datetime.now().strftime("%A")
    specials: dict[str, tuple[str, int, str]] = {
        "Monday": ("Margherita", 20, "Meatless Monday - 20% off Margherita!"),
        "Tuesday": ("Pepperoni", 15, "Two-for-Tuesday - 15% off Pepperoni!"),
        "Wednesday": ("Veggie Supreme", 25, "Wellness Wednesday - 25% off Veggie Supreme!"),
        "Thursday": ("BBQ Chicken", 10, "Throwback Thursday - 10% off BBQ Chicken!"),
        "Friday": ("Meat Lovers", 20, "TGIF - 20% off Meat Lovers!"),
        "Saturday": ("Four Cheese", 15, "Cheesy Saturday - 15% off Four Cheese!"),
        "Sunday": ("Hawaiian", 20, "Sunday Funday - 20% off Hawaiian!"),
    }

    pizza, discount, promo = specials[day]
    original_price = PIZZA_MENU[pizza]["price"]
    sale_price = original_price * (1 - discount / 100)

    return (
        f"Today's Special ({day}):\n"
        f"  {promo}\n"
        f"  {pizza}: ${original_price:.2f} -> ${sale_price:.2f}\n\n"
        f"Combo Deal: Any 2 large pizzas + drinks for $34.99!\n"
        f"Birthday Special: Free dessert pizza with any order over $30!"
    )


@tool
def cancel_order(order_id: str) -> str:
    """Cancel a pizza order if it hasn't started baking yet.

    Args:
        order_id: The order ID to cancel.

    Returns:
        Cancellation confirmation or reason why cancellation isn't possible.
    """
    if order_id not in _orders:
        return f"Order '{order_id}' not found. Please check your order ID."

    order = _orders[order_id]
    non_cancellable = {"baking", "quality_check", "out_for_delivery", "delivered"}

    if order["status"] in non_cancellable:
        return (
            f"Sorry, order {order_id} cannot be cancelled.\n"
            f"Current status: {order['status'].replace('_', ' ').title()}\n"
            f"Orders can only be cancelled before baking begins."
        )

    order["status"] = "cancelled"
    return (
        f"Order {order_id} has been cancelled.\n"
        f"A refund of ${order['total']:.2f} will be processed within 3-5 business days."
    )
