# Copyright (c) Microsoft. All rights reserved.

"""Pizza menu catalog and size pricing constants."""

from __future__ import annotations

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

# ---------------------------------------------------------------------------
# Size pricing multipliers
# ---------------------------------------------------------------------------

SIZE_MULTIPLIER: dict[str, float] = {"small": 0.8, "medium": 1.0, "large": 1.3}
