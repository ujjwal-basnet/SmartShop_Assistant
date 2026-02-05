import sqlite3
import os

DB_FILE = "smartshop_assistant.db"
IMAGES_DIR = "images"

# Make images folder if not exists
os.makedirs(IMAGES_DIR, exist_ok=True)

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Products table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        category TEXT,
        color TEXT,
        price REAL,
        description TEXT,
        image_path TEXT
    )
    """)

    # Insert sample data
    products = [
        ("Red Saree", "sari", "red", 50, "Elegant red saree", os.path.join(IMAGES_DIR, "saree_red_1.png")),
        ("Blue Saree", "sari", "blue", 55, "Beautiful blue saree", os.path.join(IMAGES_DIR, "saree_blue_1.png")),
        ("Classic Piadina", "food", None, 5, "Italian flatbread", os.path.join(IMAGES_DIR, "piadina_classic.png")),
        ("Margherita Pizza", "food", None, 12, "Delicious pizza", os.path.join(IMAGES_DIR, "pizza_margherita.png")),
    ]

    cursor.executemany("""
    INSERT OR IGNORE INTO products (name, category, color, price, description, image_path)
    VALUES (?, ?, ?, ?, ?, ?)
    """, products)

    conn.commit()
    conn.close()
    print(f"Database {DB_FILE} initialized with sample data.")

if __name__ == "__main__":
    init_db()
