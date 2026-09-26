import sqlite3
from datetime import datetime
import os


DB_PATH = os.path.join(
    os.path.dirname(__file__),
    "smriti.db"
)


def get_connection():
    return sqlite3.connect(DB_PATH)


def initialize_actions():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS actions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL,
            description TEXT NOT NULL,
            evidence TEXT,
            status TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS audit_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            action_id INTEGER NOT NULL,
            action TEXT NOT NULL,
            status TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def propose_action(
    action_type,
    description,
    evidence=None
):

    initialize_actions()

    evidence = evidence or []

    conn = get_connection()
    cursor = conn.cursor()

    created_at = datetime.now().isoformat()

    cursor.execute(
        """
        INSERT INTO actions
        (type, description, evidence, status, created_at)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            action_type,
            description,
            str(evidence),
            "PENDING_APPROVAL",
            created_at
        )
    )

    action_id = cursor.lastrowid

    conn.commit()

    cursor.execute(
        """
        SELECT id, type, description, evidence, status, created_at
        FROM actions
        WHERE id = ?
        """,
        (action_id,)
    )

    row = cursor.fetchone()

    conn.close()

    return {
        "id": row[0],
        "type": row[1],
        "description": row[2],
        "evidence": evidence,
        "status": row[4],
        "created_at": row[5]
    }


def get_pending_actions():

    initialize_actions()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, type, description, evidence, status, created_at
        FROM actions
        WHERE status = 'PENDING_APPROVAL'
        ORDER BY id DESC
        """
    )

    rows = cursor.fetchall()

    conn.close()

    return [
        {
            "id": row[0],
            "type": row[1],
            "description": row[2],
            "evidence": row[3],
            "status": row[4],
            "created_at": row[5]
        }
        for row in rows
    ]


def approve_action(action_id):

    initialize_actions()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, type, description, evidence, status, created_at
        FROM actions
        WHERE id = ?
        """,
        (action_id,)
    )

    row = cursor.fetchone()

    if row is None:
        conn.close()
        return None

    if row[4] == "APPROVED":
        conn.close()

        return {
            "id": row[0],
            "type": row[1],
            "description": row[2],
            "evidence": row[3],
            "status": row[4],
            "created_at": row[5]
        }

    cursor.execute(
        """
        UPDATE actions
        SET status = 'APPROVED'
        WHERE id = ?
        """,
        (action_id,)
    )

    timestamp = datetime.now().isoformat()

    cursor.execute(
        """
        INSERT INTO audit_log
        (action_id, action, status, timestamp)
        VALUES (?, ?, ?, ?)
        """,
        (
            action_id,
            row[2],
            "APPROVED",
            timestamp
        )
    )

    conn.commit()

    cursor.execute(
        """
        SELECT id, type, description, evidence, status, created_at
        FROM actions
        WHERE id = ?
        """,
        (action_id,)
    )

    updated = cursor.fetchone()

    conn.close()

    return {
        "id": updated[0],
        "type": updated[1],
        "description": updated[2],
        "evidence": updated[3],
        "status": updated[4],
        "created_at": updated[5]
    }


def get_audit_log():

    initialize_actions()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT action_id, action, status, timestamp
        FROM audit_log
        ORDER BY id DESC
        """
    )

    rows = cursor.fetchall()

    conn.close()

    return [
        {
            "action_id": row[0],
            "action": row[1],
            "status": row[2],
            "timestamp": row[3]
        }
        for row in rows
    ]


initialize_actions()