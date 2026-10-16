import os
import sys
from pathlib import Path
from dotenv import load_dotenv

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Paths
CORE_DIR = Path(__file__).resolve().parent
APP_DIR = CORE_DIR.parent
PROJECT_DIR = APP_DIR.parent
ROOT_DIR = PROJECT_DIR.parent

# Load .env (check backend_python/.env then root/backend/.env)
ENV_PATH = PROJECT_DIR / ".env"
if not ENV_PATH.exists():
    ENV_PATH = ROOT_DIR / "backend" / ".env"
load_dotenv(ENV_PATH)

# Server Config
PORT = int(os.getenv("PORT", 3005))
HOST = os.getenv("HOST", "0.0.0.0")

# Database Path
DB_PATH = ROOT_DIR / "backend" / "database.sqlite"
if not DB_PATH.exists():
    DB_PATH = PROJECT_DIR / "database.sqlite"
DATABASE_URL = f"sqlite:///{DB_PATH.as_posix()}"

# Upload Directory
UPLOAD_DIR = ROOT_DIR / "backend" / "uploads"
if not UPLOAD_DIR.exists():
    UPLOAD_DIR = PROJECT_DIR / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# JWT Security
JWT_SECRET = os.getenv("JWT_SECRET", "super-secret-key-123")
JWT_ALGORITHM = "HS256"

# Gemini AI Keys
raw_keys = [os.getenv("GEMINI_API_KEY", "")]
API_KEYS = [k.strip() for k in raw_keys if k and k.strip() and "YOUR_API_KEY" not in k]

# YouTube API Config
YOUTUBE_CLIENT_ID = os.getenv("YOUTUBE_CLIENT_ID", "dummy_client_id")
YOUTUBE_CLIENT_SECRET = os.getenv("YOUTUBE_CLIENT_SECRET", "dummy_client_secret")
YOUTUBE_REDIRECT_URI = os.getenv("YOUTUBE_REDIRECT_URI", f"http://localhost:{PORT}/api/youtube/callback")

# TikTok API Config
TIKTOK_CLIENT_KEY = os.getenv("TIKTOK_CLIENT_KEY", "")
TIKTOK_CLIENT_SECRET = os.getenv("TIKTOK_CLIENT_SECRET", "")
TIKTOK_REDIRECT_URI = os.getenv("TIKTOK_REDIRECT_URI", f"http://localhost:{PORT}/api/tiktok/callback")

# Google Sheets Config
GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID", "")
GOOGLE_CLIENT_EMAIL = os.getenv("GOOGLE_CLIENT_EMAIL", "")
GOOGLE_PRIVATE_KEY = os.getenv("GOOGLE_PRIVATE_KEY", "")
