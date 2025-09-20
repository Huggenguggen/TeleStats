import json
from models import insert_chat, insert_message
from datetime import datetime

def parse_telegram_json(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    chat_name = data.get("name", "Unknown Chat")
    participants = ", ".join(data.get("participants", []))
    messages = data.get("messages", [])

    # determine date range
    timestamps = [m.get("date") for m in messages if m.get("date")]
    start_date = min(timestamps) if timestamps else None
    end_date = max(timestamps) if timestamps else None

    chat_id = insert_chat(chat_name, participants, start_date, end_date)

    for msg in messages:
        sender = msg.get("from")
        text = msg.get("text") if isinstance(msg.get("text"), str) else ""
        timestamp = msg.get("date")
        insert_message(chat_id, sender, text, timestamp)

    return chat_id
