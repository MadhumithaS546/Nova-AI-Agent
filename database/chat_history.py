import sqlite3

DB_NAME = "nova_chat.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversations(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            conversation_id INTEGER,
            role TEXT,
            message TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(conversation_id)
            REFERENCES conversations(id)
        )
    """)

    conn.commit()
    conn.close()

def create_conversation(title="New Chat"):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO conversations(title) VALUES(?)",
        (title,)
    )

    conversation_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return conversation_id


def save_message(conversation_id, role, message):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO messages(
            conversation_id,
            role,
            message
        )
        VALUES(?,?,?)
    """, (conversation_id, role, message))

    conn.commit()
    conn.close()

def load_messages(conversation_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT role, message
        FROM messages
        WHERE conversation_id=?
        ORDER BY id
    """, (conversation_id,))

    messages = [
        {"role": r, "content": m}
        for r, m in cursor.fetchall()
    ]

    conn.close()

    return messages

def clear_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM chat_history")

    conn.commit()
    conn.close()

def get_conversations():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, title
        FROM conversations
        ORDER BY created_at DESC
    """)

    conversations = cursor.fetchall()

    conn.close()

    return conversations
def rename_conversation(conversation_id, title):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE conversations SET title=? WHERE id=?",
        (title, conversation_id)
    )

    conn.commit()
    conn.close()