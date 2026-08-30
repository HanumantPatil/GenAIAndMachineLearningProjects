"""Import the scraped Flipkart product CSV into the chatbot SQLite database."""

import sqlite3
import sys
from pathlib import Path

import pandas as pd

SCRIPT_DIRECTORY = Path(__file__).resolve().parent
CSV_PATH = SCRIPT_DIRECTORY / "flipkart_product_data.csv"
DATABASE_PATH = SCRIPT_DIRECTORY.parent / "App" / "db.sqlite"
PRODUCT_COLUMNS = {
    "product_link",
    "title",
    "brand",
    "price",
    "discount",
    "avg_rating",
    "total_ratings",
}


def import_products(csv_path: Path = CSV_PATH, database_path: Path = DATABASE_PATH) -> int:
    """Replace the SQLite product table with records from the product CSV."""
    if not csv_path.is_file():
        raise FileNotFoundError(f"Product CSV was not found: {csv_path}")

    products = pd.read_csv(csv_path)
    missing_columns = PRODUCT_COLUMNS.difference(products.columns)
    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"Product CSV is missing required columns: {missing}")

    database_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(database_path) as connection:
        products.to_sql("product", connection, if_exists="replace", index=False)

    return len(products)


def main() -> int:
    """Import products and report the destination database."""
    try:
        row_count = import_products()
    except (FileNotFoundError, ValueError, OSError, sqlite3.Error) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    print(f"Imported {row_count} products into {DATABASE_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())