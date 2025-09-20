from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from pathlib import Path
from database import get_connection
from database import init_db
from utils import parse_telegram_json
from datetime import datetime
from collections import Counter
from flask_cors import CORS


UPLOAD_FOLDER = Path(__file__).parent / "uploads"
UPLOAD_FOLDER.mkdir(exist_ok=True)

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

# Initialize DB
init_db()

@app.route("/api/chats/upload", methods=["POST"])
def upload_chat():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    filename = secure_filename(file.filename)
    file_path = UPLOAD_FOLDER / filename
    file.save(file_path)

    chat_id = parse_telegram_json(file_path)
    return jsonify({"message": "Upload successful", "chat_id": chat_id})

@app.route("/api/chats", methods=["GET"])
def list_chats():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM chats")
    chats = [dict(row) for row in cur.fetchall()]
    conn.close()
    return jsonify(chats)

@app.route("/api/stats/<int:chat_id>/time_series", methods=["GET"])
def time_series(chat_id):
    interval = request.args.get("interval", "month")  # "day", "month", "year"

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT timestamp FROM messages WHERE chat_id = ?", (chat_id,))
    rows = cur.fetchall()
    conn.close()

    if not rows:
        return jsonify({"labels": [], "counts": []})

    buckets = Counter()
    for (timestamp,) in rows:
        if timestamp:
            dt = datetime.fromisoformat(timestamp)
            if interval == "year":
                key = dt.strftime("%Y")
            elif interval == "month":
                key = dt.strftime("%Y-%m")
            else:
                key = dt.strftime("%Y-%m-%d")
            buckets[key] += 1

    labels = sorted(buckets.keys())
    counts = [buckets[l] for l in labels]

    return jsonify({"labels": labels, "counts": counts})


@app.route("/api/stats/<int:chat_id>/summary", methods=["GET"])
def summary(chat_id):
    conn = get_connection()
    cur = conn.cursor()

    # Total messages
    cur.execute("SELECT COUNT(*) FROM messages WHERE chat_id = ?", (chat_id,))
    total_messages = cur.fetchone()[0]

    # Distinct participants
    cur.execute("SELECT COUNT(DISTINCT sender) FROM messages WHERE chat_id = ?", (chat_id,))
    num_participants = cur.fetchone()[0]

    # Top 5 senders
    cur.execute(
        """
        SELECT sender, COUNT(*) as cnt
        FROM messages
        WHERE chat_id = ?
        GROUP BY sender
        ORDER BY cnt DESC
        LIMIT 5
        """,
        (chat_id,),
    )
    top_senders = [{"sender": row[0] or 'System', "count": row[1]} for row in cur.fetchall()]

    conn.close()

    return jsonify(
        {
            "chat_id": chat_id,
            "total_messages": total_messages,
            "num_participants": num_participants,
            "top_senders": top_senders,
        }
    )

if __name__ == "__main__":
    app.run(debug=True, port=5000)
