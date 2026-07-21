"""
Seed the SQLite database with initial product data for The Sweet Rolls.
Run: python seed.py
"""
import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "sweetrolls.db")
SCHEMA_PATH = os.path.join(BASE_DIR, "schema.sql")

PRODUCTS = [
    {
        "slug": "banana-roll",
        "name": "Banana Roll",
        "tagline": "Crispy Outside, Sweet Inside. Perfect in Everybite",
        "price": 10000,
        "description": (
            "Banana Roll adalah menu andalan The Sweet Rolls, dibuat dari pisang pilihan "
            "yang dibalut kulit lumpia super renyah lalu digoreng hingga keemasan. "
            "Rasa manis alami pisang berpadu sempurna dengan tekstur kulit yang crispy "
            "di luar dan lembut di dalam, cocok dinikmati hangat kapan saja."
        ),
        "feature1": "Crispy Pastry",
        "feature2": "Sweet Banana",
        "feature3": "Premium Quality",
        "image": "banana_roll.webp",
        "hero_bg": "#F6DE6B",
        "accent": "#E8A63B",
        "sort_order": 1,
    },
    {
        "slug": "choco-roll",
        "name": "Choco Roll",
        "tagline": "Soft Banana, Rich Chocolate. Perfectly Rolled",
        "price": 10000,
        "description": (
            "Choco Roll memadukan lembutnya pisang dengan siraman cokelat premium yang kaya "
            "rasa. Setiap gigitan menghadirkan perpaduan manis pisang dan pahit-manis cokelat "
            "yang meleleh, dibalut kulit renyah khas The Sweet Rolls."
        ),
        "feature1": "Crispy Pastry",
        "feature2": "Rich Chocolate",
        "feature3": "Premium Quality",
        "image": "choco_roll.webp",
        "hero_bg": "#F5EEC9",
        "accent": "#7A4B32",
        "sort_order": 2,
    },
    {
        "slug": "cheese-roll",
        "name": "Cheese Roll",
        "tagline": "Sweet Banana, Creamy Cheese. Perfect Golden",
        "price": 10000,
        "description": (
            "Cheese Roll menghadirkan taburan keju gurih di atas pisang manis yang dibalut "
            "kulit crispy keemasan. Perpaduan gurih dan manis yang creamy ini menjadikan "
            "Cheese Roll favorit banyak pelanggan The Sweet Rolls."
        ),
        "feature1": "Crispy Pastry",
        "feature2": "Creamy Cheese",
        "feature3": "Premium Quality",
        "image": "cheese_roll.webp",
        "hero_bg": "#FBE18B",
        "accent": "#E8743B",
        "sort_order": 3,
    },
]


def seed_database(db_path=None):
    """Create schema and insert initial products. Safe to import and call from app.py."""
    db_path = db_path or DB_PATH
    conn = sqlite3.connect(db_path)
    with open(SCHEMA_PATH, "r") as f:
        conn.executescript(f.read())

    conn.executemany(
        """
        INSERT INTO products
            (slug, name, tagline, price, description, feature1, feature2, feature3,
             image, hero_bg, accent, sort_order)
        VALUES
            (:slug, :name, :tagline, :price, :description, :feature1, :feature2, :feature3,
             :image, :hero_bg, :accent, :sort_order)
        """,
        PRODUCTS,
    )
    conn.commit()
    conn.close()
    print(f"Seeded {len(PRODUCTS)} products into {DB_PATH}")


if __name__ == "__main__":
    seed_database()
