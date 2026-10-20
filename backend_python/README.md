# 🐍 MeDownloader Python Backend (FastAPI - Modular Architecture)

ລະບົບ Backend ດ້ວຍ Python FastAPI ທີ່ຖືກຈັດໂຄງສ້າງໃໝ່ໃຫ້ເປັນລະບົບໂມດູນ (Modular Architecture) ຕາມຂອບເຂດໜ້າວຽກ (Domain-Driven Modules). ເຂົ້າໃຈງ່າຍ, ເປັນລະບຽບ, ສະອາດ ແລະ ພ້ອມສຳລັບການພັດທະນາຕໍ່ຍອດໄດ້ຢ່າງວ່ອງໄວ.

---

## 🏗️ ໂຄງສ້າງໂຟເດີແບບໂມດູນ (Modular Project Structure)

```text
backend_python/
│
├── main.py                     # Entrypoint ຫຼັກ (FastAPI app, CORS, Lifespan, Static Mounts)
├── run.bat                     # ສະຄຣິບກົດເປີດ Server ໃນ Windows ທັນທີ
├── requirements.txt            # Dependencies ທັງໝົດ
├── test_modular_api.py         # TestClient ສະຄຣິບກວດສອບທຸກໆ Endpoint ແບບອັດຕະໂນມັດ
├── .env                        # Environment Variables (Keys, Ports, OAuth)
│
└── app/
    ├── __init__.py
    ├── api.py                  # Master API Router (ລວມທຸກ router ໄວ້ກ້ອງ prefix="/api")
    │
    ├── core/                   # ⚙️ ລະບົບຫຼັກຂອງ Backend (Core Infrastructure)
    │   ├── __init__.py         # Re-export core modules
    │   ├── config.py           # ການຕັ້ງຄ່າ, Paths, Environment Vars, JWT, API Keys
    │   ├── database.py         # SQLAlchemy Engine, Base, SequelizeDateTime, get_db, init_db
    │   ├── security.py         # Bcrypt Password Hashing, JWT Tokens, Auth Guards
    │   ├── ffmpeg.py           # FFmpeg Detection, Duration Prober, Asynchronous Process Runner
    │   └── google_sheets.py    # Google Sheets Client & Auto-synchronization logic
    │
    └── modules/                # 📦 ໂມດູນແຍກຕາມກຸ່ມໜ້າວຽກ (Domain Modules)
        │
        ├── auth/               # 🔐 ລະບົບສະມາຊິກ ແລະ Authentication
        │   ├── models.py       # User table
        │   ├── schemas.py      # Pydantic schemas (Register, Login)
        │   ├── router.py       # /api/auth (register, login, me, profile)
        │   └── __init__.py
        │
        ├── posts/              # 📰 ລະບົບໂພສທ໌ ແລະ ຂ່າວສານ
        │   ├── models.py       # Post table
        │   ├── router.py       # /api/posts (/local, /remote, /:id)
        │   └── __init__.py
        │
        ├── webview/            # 🌐 ລິ້ງຄ໌ Webview & Quick Access
        │   ├── models.py       # WebviewLink table
        │   ├── schemas.py      # Schemas
        │   ├── router.py       # /api/webview-links
        │   └── __init__.py
        │
        ├── downloader/         # ⬇️ ດາວໂຫຼດວິດີໂອ / ສຽງ (yt-dlp, TikTok, Streams)
        │   ├── schemas.py      # Request schemas
        │   ├── router.py       # /api/download, /api/info, /api/progress
        │   └── __init__.py
        │
        ├── media_editor/       # 🎬 ຕັດຕໍ່ ແລະ ປະສົມວິດີໂອ/ເພງ
        │   ├── overlays.py     # FFmpeg Complex Filters (Pomodoro, Quotes, Watermarks)
        │   ├── editor_router.py      # /api/editor/merge, cancel (Ken Burns slideshow)
        │   ├── video_mixer_router.py # /api/video-mixer (Auto mix video, music, quote)
        │   ├── music_mixer_router.py # /api/music-mixer (Audio mashup & normalize)
        │   └── __init__.py
        │
        ├── social_sync/        # 📱 ເຊື່ອມຕໍ່ YouTube & TikTok Uploads
        │   ├── models.py       # YouTubeChannel, TikTokChannel tables
        │   ├── youtube_router.py # /api/youtube (OAuth2, Channels, Video Upload with progress)
        │   ├── tiktok_router.py  # /api/tiktok (PKCE OAuth, Channels, Video Direct Upload)
        │   └── __init__.py
        │
        ├── typing/             # ⌨️ ຝຶກພິມດີດ (Lessons, Results, Leaderboard, History)
        │   ├── models.py       # TypingHistory table
        │   ├── schemas.py      # Schemas
        │   ├── router.py       # /api/typing-lessons, /api/typing-results, /api/typing-leaderboard, /api/typing-history
        │   └── __init__.py
        │
        ├── learning/           # 📚 ວິດີໂອການຮຽນຮູ້ (Learning Videos)
        │   ├── schemas.py      # VideoData schema
        │   ├── router.py       # /api/learning-videos (CRUD & Google Sheets Sync)
        │   └── __init__.py
        │
        ├── chat/               # 🤖 ປັນຍາປະດິດ Gemini AI Chatbot
        │   ├── schemas.py      # ChatRequest, ChatMessage
        │   ├── router.py       # /api/chat (Multi-key rotation, Markdown images)
        │   └── __init__.py
        │
        ├── search/             # 🔍 ຄົ້ນຫາຮູບພາບ & ວິດີໂອ Stock (Pixabay API Proxy)
        │   ├── router.py       # /api/search
        │   └── __init__.py
        │
        └── lyrics/             # 🎵 ເນື້ອເພງ (Lyrics Scraper & Search)
            ├── schemas.py      # SongLyricsRequest
            ├── router.py       # /api/lyrics (home, search, song)
            └── __init__.py
```

---

## 🚀 ວິທີການເປີດໃຊ້ງານ (How to Run)

### ວິທີທີ 1: Double Click (Windows)
ກົດ Run ໄຟລ໌:
```cmd
run.bat
```

### ວິທີທີ 2: ເປີດຜ່ານ Terminal
```powershell
cd backend_python
.\venv\Scripts\python.exe main.py
```

- **API Base URL:** `http://localhost:3005/api`
- **Swagger Documentation (Interactive UI):** `http://localhost:3005/docs`
- **ReDoc Documentation:** `http://localhost:3005/redoc`

---

## 🧪 ການທົດສອບລະບົບ (Running Tests)

ທ່ານສາມາດກວດສອບຄວາມຖືກຕ້ອງຂອງທຸກໂມດູນໄດ້ງ່າຍໆດ້ວຍຄຳສັ່ງ:
```powershell
.\venv\Scripts\python.exe test_modular_api.py
```

---

## 💡 ວິທີເພີ່ມໂມດູນໃໝ່ໃນອະນາຄົດ (How to Add a New Module)

ເມື່ອຕ້ອງການເພີ່ມ Feature ໃໝ່:
1. ສ້າງໂຟເດີໃໝ່ໃນ `app/modules/<ຊື່ໂມດູນ>/` ເຊັ່ນ: `app/modules/notifications/`
2. ສ້າງໄຟລ໌:
   - `models.py` (ຖ້າມີ Database Table)
   - `schemas.py` (ຖ້າມີ Request/Response validation)
   - `router.py` (ກຳນົດ Endpoints)
   - `__init__.py` (Export router)
3. ນຳເຂົ້າ Router ໄປລົງທະບຽນໃນ `app/api.py`:
   ```python
   from app.modules.notifications import notifications_router
   api_router.include_router(notifications_router)
   ```
ທຸກຢ່າງຈະຖືກເຊື່ອມຕໍ່ເຂົ້າສູ່ລະບົບຫຼັກໂດຍອັດຕະໂນມັດ ໂດຍບໍ່ລົບກວນໂມດູນອື່ນ!
