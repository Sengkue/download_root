from routers.auth import router as auth_router
from routers.posts import router as posts_router
from routers.webview import router as webview_router
from routers.typing import router as typing_router
from routers.typing_history import router as typing_history_router
from routers.learning_videos import router as learning_videos_router
from routers.chat import router as chat_router
from routers.search import router as search_router
from routers.lyrics import router as lyrics_router
from routers.download import router as download_router
from routers.editor import router as editor_router
from routers.video_mixer import router as video_mixer_router
from routers.music_mixer import router as music_mixer_router
from routers.youtube import router as youtube_router
from routers.tiktok import router as tiktok_router

__all__ = [
    "auth_router",
    "posts_router",
    "webview_router",
    "typing_router",
    "typing_history_router",
    "learning_videos_router",
    "chat_router",
    "search_router",
    "lyrics_router",
    "download_router",
    "editor_router",
    "video_mixer_router",
    "music_mixer_router",
    "youtube_router",
    "tiktok_router"
]
