import os
import secrets
import hashlib
import urllib.parse
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
import httpx

from app.core.config import TIKTOK_CLIENT_KEY, TIKTOK_CLIENT_SECRET, TIKTOK_REDIRECT_URI
from app.core.database import get_db
from app.core.ffmpeg import progress_map
from app.modules.social_sync.models import TikTokChannel

router = APIRouter(prefix="/tiktok", tags=["TikTok Integration"])

pkce_store = {}

@router.get("/auth")
def get_auth_url():
    csrf_state = secrets.token_hex(16)
    code_verifier = secrets.token_hex(32)
    code_challenge = hashlib.sha256(code_verifier.encode("utf-8")).hexdigest()

    pkce_store[csrf_state] = code_verifier

    params = {
        "client_key": TIKTOK_CLIENT_KEY,
        "scope": "user.info.basic,video.publish,video.upload",
        "response_type": "code",
        "redirect_uri": TIKTOK_REDIRECT_URI,
        "state": csrf_state,
        "code_challenge": code_challenge,
        "code_challenge_method": "S256"
    }
    url = f"https://www.tiktok.com/v2/auth/authorize/?{urllib.parse.urlencode(params)}"
    return {"url": url}

@router.get("/callback")
async def auth_callback(
    code: str = Query(None),
    state: str = Query(None),
    error: str = Query(None),
    db: Session = Depends(get_db)
):
    if error:
        raise HTTPException(status_code=400, detail="Authentication failed or was cancelled.")
    if not code:
        raise HTTPException(status_code=400, detail="No code provided")

    code_verifier = pkce_store.pop(state, None)
    if not code_verifier:
        raise HTTPException(status_code=400, detail="Invalid state or session expired.")

    token_data = {
        "client_key": TIKTOK_CLIENT_KEY,
        "client_secret": TIKTOK_CLIENT_SECRET,
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": TIKTOK_REDIRECT_URI,
        "code_verifier": code_verifier
    }

    async with httpx.AsyncClient(timeout=20.0) as client:
        try:
            token_res = await client.post(
                "https://open.tiktokapis.com/v2/oauth/token/",
                data=token_data,
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )
            tokens = token_res.json()
            if tokens.get("error"):
                raise HTTPException(status_code=400, detail=tokens.get("error_description", "Failed to get token"))

            access_token = tokens.get("access_token")
            refresh_token = tokens.get("refresh_token")
            expires_in = tokens.get("expires_in", 86400)
            token_expiry = datetime.now(timezone.utc) + timedelta(seconds=expires_in)

            user_res = await client.get(
                "https://open.tiktokapis.com/v2/user/info/?fields=open_id,union_id,avatar_url,display_name",
                headers={"Authorization": f"Bearer {access_token}"}
            )
            user_data = user_res.json().get("data", {}).get("user", {})

            channel_id = user_data.get("open_id") or user_data.get("union_id")
            channel_title = user_data.get("display_name", "TikTok User")
            thumbnail_url = user_data.get("avatar_url", "")

            tk_channel = db.query(TikTokChannel).filter(TikTokChannel.channelId == channel_id).first()
            if not tk_channel:
                tk_channel = TikTokChannel(
                    channelId=channel_id,
                    channelTitle=channel_title,
                    thumbnailUrl=thumbnail_url,
                    accessToken=access_token,
                    refreshToken=refresh_token,
                    tokenExpiry=token_expiry
                )
                db.add(tk_channel)
            else:
                tk_channel.channelTitle = channel_title
                tk_channel.thumbnailUrl = thumbnail_url
                tk_channel.accessToken = access_token
                if refresh_token:
                    tk_channel.refreshToken = refresh_token
                tk_channel.tokenExpiry = token_expiry

            db.commit()
            return RedirectResponse("http://localhost:3000/editor/video-mixer?tiktok_auth=success")
        except Exception as e:
            print(f"TikTok Auth Error: {e}")
            raise HTTPException(status_code=500, detail=str(e))

@router.get("/channels")
def get_connected_channels(db: Session = Depends(get_db)):
    channels = db.query(TikTokChannel).all()
    return [
        {
            "id": c.id,
            "channelId": c.channelId,
            "channelTitle": c.channelTitle,
            "thumbnailUrl": c.thumbnailUrl
        }
        for c in channels
    ]

class TikTokUploadRequest(BaseModel):
    channelId: str
    videoPath: str
    title: str = ""
    tags: str = None
    jobId: str = None

@router.post("/upload")
async def upload_video(data: TikTokUploadRequest, db: Session = Depends(get_db)):
    if not data.channelId or not data.videoPath or not os.path.exists(data.videoPath):
        raise HTTPException(status_code=400, detail="Missing required fields or video not found.")

    tk_channel = db.query(TikTokChannel).filter(TikTokChannel.channelId == data.channelId).first()
    if not tk_channel:
        raise HTTPException(status_code=404, detail="Channel not found in database.")

    file_size = os.path.getsize(data.videoPath)

    if data.jobId:
        progress_map[data.jobId] = {"progress": 10, "status": "Initializing upload..."}

    tag_str = ""
    if data.tags:
        tags = [f"#{t.strip().lstrip('#')}" for t in data.tags.split(",") if t.strip()]
        tag_str = " " + " ".join(tags)

    init_payload = {
        "post_info": {
            "title": f"{data.title}{tag_str}".strip(),
            "privacy_level": "SELF_ONLY",
            "disable_duet": False,
            "disable_comment": False,
            "disable_stitch": False,
            "video_cover_timestamp_ms": 1000
        },
        "source_info": {
            "source": "FILE_UPLOAD",
            "video_size": file_size,
            "chunk_size": file_size,
            "total_chunk_count": 1
        }
    }

    async with httpx.AsyncClient(timeout=120.0) as client:
        try:
            init_res = await client.post(
                "https://open.tiktokapis.com/v2/post/publish/video/init/",
                json=init_payload,
                headers={
                    "Authorization": f"Bearer {tk_channel.accessToken}",
                    "Content-Type": "application/json"
                }
            )
            init_data = init_res.json()
            if init_data.get("error") and init_data["error"].get("code") != "ok":
                raise HTTPException(status_code=400, detail=init_data["error"].get("message", "Failed to init upload"))

            upload_url = init_data["data"]["upload_url"]
            publish_id = init_data["data"]["publish_id"]

            if data.jobId:
                progress_map[data.jobId] = {"progress": 30, "status": "Uploading to TikTok..."}

            with open(data.videoPath, "rb") as vf:
                file_content = vf.read()

            put_res = await client.put(
                upload_url,
                content=file_content,
                headers={
                    "Content-Type": "video/mp4",
                    "Content-Range": f"bytes 0-{file_size - 1}/{file_size}"
                }
            )

            if put_res.status_code not in [200, 201]:
                raise HTTPException(status_code=put_res.status_code, detail="Failed to upload video stream to TikTok")

            if data.jobId:
                progress_map[data.jobId] = {"progress": 100, "status": "Upload complete!"}

            return {
                "success": True,
                "publishId": publish_id,
                "message": "Upload initiated successfully. It may take a moment to process on TikTok."
            }
        except Exception as e:
            print(f"TikTok Upload Error: {e}")
            raise HTTPException(status_code=500, detail=str(e))
