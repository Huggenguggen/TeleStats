# 📊 Telegram Chat Analyzer – TeleStats

## ✅ Accomplishments

### **Frontend (Nuxt 4 + TailwindCSS)**

* Initialized Nuxt 4 app with TailwindCSS.
* Implemented **DropZone component** (`useDropZone` from `@vueuse/core`):

  * Drag & drop + click-to-upload.
  * File preview (name + size).
  * Upload button with loading state + error handling.
  * On success → redirects to `/chat/:chat_id`.
* Created **Chat Dashboard (`/chat/[id].vue`)**:

  * Fetches stats from backend.
  * Displays **line chart** of messages over time (Chart.js).
  * Shows **summary stats** (total messages, participants, top senders).
  * Replaces `NULL` senders with `"System"` for cleaner display.
* Added **Chat Search Component (`ChatSearch.vue`)**:

  * Fetches all uploaded chats from backend.
  * Filters by name or ID.
  * Click or press Enter → redirects to `/chat/[id]`.
* Added **Navbar Component (`Navbar.vue`)**:

  * Left: clickable “TeleStats” → home page.
  * Right: Chat search bar dropdown for quick navigation.
* Integrated components in `app.vue` for consistent header/navigation across pages.

---

### **Backend (Flask + SQLite)**

* Flask API with routes:

  * `POST /api/chats/upload` → Upload Telegram JSON, parse, save to DB, return `chat_id`.
  * `GET /api/chats` → List uploaded chats (used by search component).
  * `GET /api/stats/<chat_id>/summary` → Total messages, participants, top senders.
  * `GET /api/stats/<chat_id>/time_series?interval=month` → Messages over time.
* `flask-cors` integrated → allows frontend (`localhost:3000`) to call backend (`localhost:5000`).
* File uploads stored under `uploads/`.
* Database initialized automatically at startup.
* Replaces `NULL` senders with `"System"` when returning top senders.

---

### **Database (SQLite)**

* Tables:

  * `chats` → metadata of uploaded chats.
  * `messages` → individual messages (chat\_id, sender, text, timestamp, word count).
* Indexing for performance (`chat_id`, `sender`, `timestamp`).
* Auto-initialized at runtime; DB stored in `backend/telegram_analyzer/db/telegram.db`.

---

### **Infrastructure**

* **Dockerized** both frontend and backend.
* **docker-compose.yml** at project root:

  * `frontend` service → Nuxt (port 3000).
  * `backend` service → Flask (port 5000).
  * Volumes for uploads + SQLite DB persistence.
* Ready for local development and easy deployment.

---

### **Project Structure**

```
telestats/
├── backend/
│   └── telegram_analyzer/
│       ├── app.py               # Flask entrypoint
│       ├── database.py          # SQLite connection + schema
│       ├── utils.py             # Telegram JSON parsing
│       ├── uploads/             # Uploaded chat JSON files
│       └── db/
│           └── telegram.db      # SQLite database (mounted volume)
├── frontend/
│   └── app/
│       ├── app.vue              # Nuxt 4 root layout
│       ├── assets/              # TailwindCSS, images, styles, etc.
│       ├── components/
│       │   ├── DropZone.vue
│       │   ├── ChatSearch.vue
│       │   └── Navbar.vue
│       ├── composables/         # Custom composables (hooks)
│       └── pages/
│           ├── index.vue        # Upload page
│           └── chat/[id].vue    # Dashboard page
│   └── .env                     # API base config
├── docker-compose.yml
├── README.md

```

---

### **Next Steps / TODO**

* Add additional analytics (e.g., most used words, emoji stats).
* Enhance chart visualizations (daily/weekly breakdown, rolling averages).
* Add authentication or multi-user support.
* Improve UI/UX: responsive navbar, better dropdown styling.
* Add unit tests / e2e tests for frontend and backend.
* Consider backend optimizations for very large chat exports.

---

If you want, I can also make a **one-page “visual overview” diagram** of the architecture and flow from upload → database → dashboard → search for your README. It would make this summary even more intuitive. Do you want me to do that next?
