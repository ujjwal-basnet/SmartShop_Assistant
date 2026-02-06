import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DB_PATH = BASE_DIR / "db" / "smartshop_assistant.db"
IMAGES_DIR = BASE_DIR / "db" / "images"
IMAGES_DIR.mkdir(parents=True, exist_ok=True)

PRODUCTS_SEED = [
    (
        1,
        "Black T-Shirt",
        "apparel:tshirt",
        "black",
        12.99,
        "Plain black short-sleeve cotton T-shirt, solid color, crew neck, minimal design, unisex casual everyday wear.",
        10,
        str(IMAGES_DIR / "black-tshirt.jpg"),
    ),
    (
        2,
        "Blue T-Shirt",
        "apparel:tshirt",
        "blue",
        12.99,
        "Solid blue short-sleeve T-shirt, smooth fabric, crew neck, simple casual and sporty look for daily wear.",
        10,
        str(IMAGES_DIR / "blue_tshirt.jpeg"),
    ),
    (
        3,
        "Colgate MaxWhite Toothpaste",
        "grocery:toiletries",
        None,
        2.49,
        "Colgate MaxWhite toothpaste tube with white/red branding, mint freshness style oral care for cleaning and whitening teeth.",
        25,
        str(IMAGES_DIR / "colgate.jpg"),
    ),
    (
        4,
        "Doritos Nacho Cheese Chips",
        "grocery:snacks",
        None,
        1.99,
        "Doritos Nacho Cheese chips in red packet, crunchy triangular corn chips, savory snack suitable for parties and sharing.",
        30,
        str(IMAGES_DIR / "doritos.jpg"),
    ),
    (
        5,
        "Lay's Classic Potato Chips",
        "grocery:snacks",
        None,
        1.79,
        "Lay's Classic potato chips in yellow packet, thin sliced crispy salted chips, light crunchy snack for casual eating.",
        35,
        str(IMAGES_DIR / "lays.jpg"),
    ),
    (
        6,
        "Parle Magix Mango Biscuits",
        "grocery:snacks",
        None,
        1.49,
        "Parle Magix mango cream sandwich biscuits pack, sweet biscuit snack with mango-flavored cream filling.",
        20,
        str(IMAGES_DIR / "magix.jpg"),
    ),
    (
        7,
        "Red T-Shirt",
        "apparel:tshirt",
        "red",
        12.99,
        "Bright red short-sleeve T-shirt, solid color, crew neck, clean minimal casual clothing for everyday use.",
        10,
        str(IMAGES_DIR / "red_tshirt.jpg"),
    ),
    (
        8,
        "Sunglasses (Black/Gold)",
        "accessory:sunglasses",
        None,
        9.99,
        "Black sunglasses with gold frame accents and dark tinted lenses, stylish fashion accessory for outdoor sun protection.",
        15,
        str(IMAGES_DIR / "sunnglasses.jpg"),
    ),
]

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        category TEXT,
        color TEXT,
        price REAL,
        description TEXT,
        quantity INTEGER DEFAULT 0,
        image_path TEXT
    )
    """)

    count = cur.execute("SELECT COUNT(*) FROM products").fetchone()[0]
    if count == 0:
        cur.executemany("""
        INSERT INTO products (id, name, category, color, price, description, quantity, image_path)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, PRODUCTS_SEED)
        print(f"Database initialized: {DB_PATH}")
    else:
        print(f"Database already has data ({count} rows). Skipping seed.")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
