import os
import sys
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn

import asyncio

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

if sys.platform == "win32":
    try:
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    except Exception:
        pass

from app.core.config import PORT, HOST, UPLOAD_DIR
from app.core.database import init_db
from app.core.google_sheets import connect_google_sheets
from app.api import api_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize Database & Google Sheets
    init_db()
    connect_google_sheets()
    print(f"[OK] Dedicated Python FastAPI Backend running on http://localhost:{PORT}")
    yield
    # Shutdown

app = FastAPI(
    title="MeDownloader Python Backend",
    description="High-performance Python FastAPI backend for MeDownloader",
    version="2.0.0",
    lifespan=lifespan
)

# CORS configuration matching Nuxt frontend requirements
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition", "Content-Length", "X-Video-Path"]
)

# Serve static uploads
app.mount("/uploads", StaticFiles(directory=str(UPLOAD_DIR)), name="uploads")

# Mount master API router under /api
app.include_router(api_router)

@app.get("/")
def root():
    return {
        "status": "online",
        "service": "MeDownloader Python Backend (Modular Architecture)",
        "version": "2.0.0",
        "docs": "/docs"
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host=HOST, port=PORT, reload=True)
