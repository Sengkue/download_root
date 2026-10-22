from fastapi import APIRouter

# Import all module routers
from app.modules.auth import auth_router
from app.modules.posts import posts_router
from app.modules.webview import webview_router
from app.modules.typing import typing_router
from app.modules.learning import learning_router
from app.modules.chat import chat_router
from app.modules.search import search_router
from app.modules.lyrics import lyrics_router
from app.modules.downloader import downloader_router
from app.modules.media_editor import editor_router, video_mixer_router, music_mixer_router
from app.modules.social_sync import youtube_router, tiktok_router
from app.modules.meta_music import meta_music_router
from app.modules.tts import tts_router

# Master API Router with /api prefix
api_router = APIRouter(prefix="/api")

# Include all domain module routers
api_router.include_router(auth_router)
api_router.include_router(posts_router)
api_router.include_router(webview_router)
api_router.include_router(chat_router)
api_router.include_router(search_router)
api_router.include_router(lyrics_router)
api_router.include_router(learning_router)
api_router.include_router(editor_router)
api_router.include_router(video_mixer_router)
api_router.include_router(music_mixer_router)
api_router.include_router(youtube_router)
api_router.include_router(tiktok_router)
api_router.include_router(meta_music_router)
api_router.include_router(tts_router)

# Direct root-level routes under /api (e.g. /api/download, /api/typing-lessons)
api_router.include_router(downloader_router)
api_router.include_router(typing_router)

__all__ = ["api_router"]
