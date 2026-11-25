
import sqlite3
from config import DATABASE_PATH


def get_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def create_tables():
    connection = get_connection()

    cursor = connection.cursor()

    # Store customer conversations
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Store individual chat messages
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (session_id)
            REFERENCES conversations(session_id)
        )
    """)

    # Store mock customer orders
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            order_id TEXT PRIMARY KEY,
            customer_name TEXT NOT NULL,
            status TEXT NOT NULL,
            estimated_delivery TEXT
        )
    """)

    # Store customer support tickets
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            ticket_id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id TEXT NOT NULL,
            subject TEXT NOT NULL,
            description TEXT NOT NULL,
            status TEXT DEFAULT 'Open',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Insert sample orders
    sample_orders = [
        ("ORD1001", "Rahul", "Shipped", "2026-11-27"),
        ("ORD1002", "Priya", "Processing", "2026-11-29"),
        ("ORD1003", "Arjun", "Delivered", "2026-11-22")
    ]

    cursor.executemany("""
        INSERT OR IGNORE INTO orders
        (order_id, customer_name, status, estimated_delivery)
        VALUES (?, ?, ?, ?)
    """, sample_orders)


    connection.commit()
    connection.close()

    print("Database tables created successfully!")

def save_message(session_id, role, content):
    connection = get_connection()
    cursor = connection.cursor()

    # Ensure conversation exists
    cursor.execute("""
        INSERT OR IGNORE INTO conversations (session_id)
        VALUES (?)
    """, (session_id,))

    # Save message
    cursor.execute("""
        INSERT INTO messages (session_id, role, content)
        VALUES (?, ?, ?)
    """, (session_id, role, content))

    connection.commit()
    connection.close()


def get_chat_history(session_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT role, content, created_at
        FROM messages
        WHERE session_id = ?
        ORDER BY id
    """, (session_id,))

    messages = cursor.fetchall()
    connection.close()

    return messages



if __name__ == "__main__":
    create_tables()
