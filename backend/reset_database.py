import sqlite3

DB_PATH = "smriti.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("DELETE FROM memories")
cursor.execute("DELETE FROM messages")

cursor.execute(
    "DELETE FROM sqlite_sequence WHERE name='messages'"
)

cursor.execute(
    "DELETE FROM sqlite_sequence WHERE name='memories'"
)

conn.commit()
conn.close()

print("Database reset successfully.")