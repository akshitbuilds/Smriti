import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "smriti.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def create_database():
    conn = get_connection()
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

    # Human-in-the-loop actions Smriti proposes (e.g. "send a reminder
    # to Rohan"). A human must approve before anything is considered done.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS actions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT,
            description TEXT,
            evidence TEXT,
            status TEXT DEFAULT 'PENDING',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            approved_at TEXT
        )
    """)

    # Every approval is written here so there is a visible trail.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS audit_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            action TEXT,
            status TEXT,
            timestamp TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def message_count():
    conn = get_connection()
    count = conn.execute("SELECT COUNT(*) AS c FROM messages").fetchone()["c"]
    conn.close()
    return count


def save_messages(messages):
    conn = get_connection()
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


def get_all_messages():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM messages ORDER BY id ASC").fetchall()
    conn.close()
    return [dict(row) for row in rows]


def save_memories(memories):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM memories")

    for m in memories:
        cursor.execute("""
            INSERT INTO memories
            (type, statement, owner, deadline, source_message_id,
             source_quote, confidence, verified)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            m["type"], m["statement"], m["owner"], m["deadline"],
            m["source_message_id"], m["source_quote"], m["confidence"],
            1 if m["verified"] else 0,
        ))

    conn.commit()
    conn.close()


def get_all_memories():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM memories ORDER BY id ASC").fetchall()
    conn.close()
    return [dict(row) for row in rows]


def create_action(type_, description, evidence):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO actions (type, description, evidence, status)
        VALUES (?, ?, ?, 'PENDING')
    """, (type_, description, str(evidence)))
    conn.commit()
    action_id = cursor.lastrowid
    conn.close()
    return action_id


def get_pending_actions():
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM actions WHERE status = 'PENDING' ORDER BY id DESC"
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def approve_action(action_id):
    conn = get_connection()
    cursor = conn.cursor()
    row = cursor.execute(
        "SELECT * FROM actions WHERE id = ?", (action_id,)
    ).fetchone()

    if row is None:
        conn.close()
        return None

    cursor.execute("""
        UPDATE actions
        SET status = 'APPROVED', approved_at = CURRENT_TIMESTAMP
        WHERE id = ?
    """, (action_id,))

    cursor.execute("""
        INSERT INTO audit_log (action, status)
        VALUES (?, 'APPROVED')
    """, (row["description"],))

    conn.commit()
    conn.close()
    return action_id


def get_audit_log():
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM audit_log ORDER BY id DESC"
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]
