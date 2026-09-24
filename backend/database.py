import sqlite3


DB_PATH = "smriti.db"


def create_database():
    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            sender TEXT,
            text TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS memories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT,
            statement TEXT,
            owner TEXT,
            deadline TEXT,
            source_message_id INTEGER,
            source_quote TEXT,
            confidence REAL,
            verified INTEGER
        )
    """)

    conn.commit()
    conn.close()


def save_messages(messages):
    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    for message in messages:
        cursor.execute("""
            INSERT INTO messages
            (timestamp, sender, text)
            VALUES (?, ?, ?)
        """, (
            message["timestamp"],
            message["sender"],
            message["text"]
        ))

    conn.commit()
    conn.close()