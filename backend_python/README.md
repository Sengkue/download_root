# 🐍 MeDownloader Python Backend (FastAPI)

Modern, high-performance Python backend replacing the previous Node.js Express backend with 100% API compatibility for the Nuxt frontend.

## 🚀 Key Advantages of Python for this Backend
1. **Native yt-dlp**: Native Python implementation of `yt-dlp` eliminates process wrapper overhead and provides robust video/audio extraction.
2. **FastAPI & Async**: High performance with asynchronous endpoints and automated interactive documentation at `/docs`.
3. **Bundled FFmpeg**: Uses `imageio-ffmpeg` to provide clean FFmpeg execution for video transitions, ken burns slideshows, pomodoro overlays, audio mixing, and quote rendering.
4. **Zero Frontend Changes**: Serves on the exact same port (`http://localhost:3005`) and exposes identical `/api/...` endpoints and CORS headers (`X-Video-Path`, `Content-Disposition`, `Content-Length`).

---

## 🛠️ Installation & Quick Start

### Option 1: Quick Run (Windows)
Double click or run:
```cmd
run.bat
```

### Option 2: Manual Terminal Run
```powershell
cd backend_python

# Activate virtual environment
.\venv\Scripts\activate

# Run FastAPI dev server
python main.py
```

The backend will start at:
- **API Base:** `http://localhost:3005/api`
- **Interactive Swagger Documentation:** `http://localhost:3005/docs`
- **ReDoc Documentation:** `http://localhost:3005/redoc`

---

## 📂 Project Structure
- `main.py`: Main FastAPI application, CORS configuration, static `/uploads` mount, router registration.
- `config/`:
  - `database.py`: SQLAlchemy setup with `SequelizeDateTime` compatibility for the shared SQLite database.
  - `google_sheets.py`: Google Sheets service account integration for real-time webview links, typing lessons, and learning videos.
  - `ffmpeg_utils.py`: FFmpeg executable detection, audio/video duration probing, and asynchronous command runner with SSE progress tracking.
  - `overlay_filters.py`: Complex FFmpeg filter graph builder for Pomodoro timer, dynamic quotes, watermarks, and playlist highlights.
  - `api_keys.py`: Google Gemini API key rotation manager.
- `models/`: SQLAlchemy models matching SQLite tables (`Users`, `Posts`, `WebviewLinks`, `TypingHistories`, `youtube_channels`, `tiktok_channels`).
- `middlewares/`: JWT authentication and password hashing utilities.
- `routers/`:
  - `auth.py`: `/api/auth/register`, `/api/auth/login`, `/api/auth/me`
  - `posts.py`: `/api/posts`, `/api/posts/local`
  - `webview.py`: `/api/webview-links` (Google Sheets + SQLite fallback)
  - `typing.py`: `/api/typing-lessons`, `/api/typing-result`, `/api/typing-leaderboard`
  - `typing_history.py`: `/api/typing-history`
  - `learning_videos.py`: `/api/learning-videos`
  - `chat.py`: `/api/chat` (Gemini AI with key rotation)
  - `search.py`: `/api/search` (Pixabay proxy)
  - `lyrics.py`: `/api/lyrics/home`, `/api/lyrics/search`, `/api/lyrics/song`
  - `download.py`: `/api/info`, `/api/download`, `/api/progress` (yt-dlp, TikTok, SSE stream)
  - `editor.py`: `/api/editor/merge`, `/api/editor/cancel` (Ken Burns slideshow generator)
  - `video_mixer.py`: `/api/video-mixer`, cancel
  - `music_mixer.py`: `/api/music-mixer/mix`
  - `youtube.py`: `/api/youtube/auth`, `/api/youtube/callback`, `/api/youtube/channels`, `/api/youtube/upload`
  - `tiktok.py`: `/api/tiktok/auth`, `/api/tiktok/callback`, `/api/tiktok/channels`, `/api/tiktok/upload`
