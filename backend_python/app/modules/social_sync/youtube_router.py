import os
from datetime import datetime, timezone
from pathlib import Path
from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

from app.core.config import YOUTUBE_CLIENT_ID, YOUTUBE_CLIENT_SECRET, YOUTUBE_REDIRECT_URI
from app.core.database import get_db
from app.core.ffmpeg import progress_map
from app.modules.social_sync.models import YouTubeChannel

router = APIRouter(prefix="/youtube", tags=["YouTube Integration"])

SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube.readonly"
]

def get_flow():
    client_config = {
        "web": {
            "client_id": YOUTUBE_CLIENT_ID,
            "client_secret": YOUTUBE_CLIENT_SECRET,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": [YOUTUBE_REDIRECT_URI]
        }
    }
    return Flow.from_client_config(client_config, scopes=SCOPES, redirect_uri=YOUTUBE_REDIRECT_URI)

@router.get("/auth")
def get_auth_url():
    flow = get_flow()
    auth_url, _ = flow.authorization_url(access_type="offline", prompt="consent")
    return {"url": auth_url}

@router.get("/callback")
def auth_callback(code: str = Query(None), db: Session = Depends(get_db)):
    if not code:
        raise HTTPException(status_code=400, detail="No code provided")

    try:
        flow = get_flow()
        flow.fetch_token(code=code)
        creds = flow.credentials

        youtube = build("youtube", "v3", credentials=creds)
        res = youtube.channels().list(part="snippet", mine=True).execute()

        items = res.get("items", [])
        if not items:
            raise HTTPException(status_code=404, detail="No YouTube channel found for this account.")

        channel = items[0]
        channel_id = channel.get("id")
        snippet = channel.get("snippet", {})
        channel_title = snippet.get("title", "")
        thumbnail_url = snippet.get("thumbnails", {}).get("default", {}).get("url", "")

        yt_channel = db.query(YouTubeChannel).filter(YouTubeChannel.channelId == channel_id).first()
        if not yt_channel:
            yt_channel = YouTubeChannel(
                channelId=channel_id,
                channelTitle=channel_title,
                thumbnailUrl=thumbnail_url,
                accessToken=creds.token,
                refreshToken=creds.refresh_token,
                tokenExpiry=creds.expiry
            )
            db.add(yt_channel)
        else:
            yt_channel.channelTitle = channel_title
            yt_channel.thumbnailUrl = thumbnail_url
            yt_channel.accessToken = creds.token
            if creds.refresh_token:
                yt_channel.refreshToken = creds.refresh_token
            if creds.expiry:
                yt_channel.tokenExpiry = creds.expiry

        db.commit()
        return RedirectResponse("http://localhost:3000/editor/video-mixer?youtube_auth=success")
    except Exception as e:
        print(f"YouTube Auth Error: {e}")
        raise HTTPException(status_code=500, detail=f"Authentication failed: {str(e)}")

@router.get("/channels")
def get_connected_channels(db: Session = Depends(get_db)):
    channels = db.query(YouTubeChannel).all()
    return [
        {
            "id": c.id,
            "channelId": c.channelId,
            "channelTitle": c.channelTitle,
            "thumbnailUrl": c.thumbnailUrl
        }
        for c in channels
    ]

class UploadVideoRequest(BaseModel):
    channelId: str
    videoPath: str
    title: str = ""
    description: str = ""
    tags: str = None
    privacyStatus: str = "private"
    jobId: str = None

@router.post("/upload")
def upload_video(data: UploadVideoRequest, db: Session = Depends(get_db)):
    if not data.channelId or not data.videoPath or not os.path.exists(data.videoPath):
        raise HTTPException(status_code=400, detail="Missing required fields or video not found.")

    yt_channel = db.query(YouTubeChannel).filter(YouTubeChannel.channelId == data.channelId).first()
    if not yt_channel:
        raise HTTPException(status_code=404, detail="Channel not found in database.")

    creds = Credentials(
        token=yt_channel.accessToken,
        refresh_token=yt_channel.refreshToken,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=YOUTUBE_CLIENT_ID,
        client_secret=YOUTUBE_CLIENT_SECRET
    )

    try:
        youtube = build("youtube", "v3", credentials=creds)

        tag_list = [t.strip() for t in data.tags.split(",") if t.strip()] if data.tags else []

        body = {
            "snippet": {
                "title": data.title,
                "description": data.description,
                "tags": tag_list,
                "categoryId": "22"
            },
            "status": {
                "privacyStatus": data.privacyStatus,
                "selfDeclaredMadeForKids": False
            }
        }

        media = MediaFileUpload(data.videoPath, chunksize=1024*1024, resumable=True)
        request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)

        if data.jobId:
            progress_map[data.jobId] = {"progress": 0, "status": "Starting YouTube upload..."}

        response = None
        while response is None:
            status_val, response = request.next_chunk()
            if status_val and data.jobId:
                pct = round(status_val.progress() * 100)
                progress_map[data.jobId] = {"progress": pct, "status": "Uploading to YouTube..."}

        video_id = response.get("id")
        if data.jobId:
            progress_map[data.jobId] = {"progress": 100, "status": "Upload complete!"}

        return {"url": f"https://youtu.be/{video_id}"}
    except Exception as e:
        print(f"YouTube Upload Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
