from database import get_connection

def insert_chat(name, participants, start_date, end_date):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO chats (name, participants, start_date, end_date) VALUES (?, ?, ?, ?)",
        (name, participants, start_date, end_date)
    )
    chat_id = cur.lastrowid
    conn.commit()
    conn.close()
    return chat_id

def insert_message(chat_id, sender, text, timestamp):
    word_count = len(text.split()) if text else 0
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO messages (chat_id, sender, text, timestamp, word_count) VALUES (?, ?, ?, ?, ?)",
        (chat_id, sender, text, timestamp, word_count)
    )
    conn.commit()
    conn.close()
