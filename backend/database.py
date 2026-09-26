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


def get_messages():
    conn = sqlite3.connect(DB_PATH)

    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, timestamp, sender, text
        FROM messages
        ORDER BY timestamp
    """)

    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]


def save_memory(memory, confidence=0.95):
    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO memories
        (
            type,
            statement,
            owner,
            deadline,
            source_message_id,
            source_quote,
            confidence,
            verified
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        memory["type"],
        memory["statement"],
        memory["owner"],
        memory["deadline"],
        memory["source_message_id"],
        memory["source_quote"],
        confidence,
        1
    ))

    conn.commit()
    conn.close()


def get_memories():
    conn = sqlite3.connect(DB_PATH)

    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM memories
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]