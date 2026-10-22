import os
import uuid
import json
import base64
from pathlib import Path
from typing import Optional, List, Dict, Any
from fastapi import APIRouter, HTTPException, Query, Response, UploadFile, File, Form
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.core.config import UPLOAD_DIR
from app.modules.tts.service import (
    generate_speech_audio_async,
    list_elevenlabs_voices,
    get_elevenlabs_user_info,
    eleven_client,
    lao_to_thai,
    hmong_to_phonetic
)

router = APIRouter(prefix="/tts", tags=["TTS & Podcast Studio"])

PODCAST_VIDEOS_DIR = UPLOAD_DIR / "podcast_videos"
PODCAST_VIDEOS_DIR.mkdir(parents=True, exist_ok=True)

class SynthesizePayload(BaseModel):
    text: str
    lang: str = "lo"
    gender: str = "male"
    voice_id: Optional[str] = None
    engine: str = "elevenlabs"

@router.get("/user-status")
def user_status():
    """Returns ElevenLabs plan, credit quota, and usage."""
    return get_elevenlabs_user_info()

@router.get("/voices")
def get_voices():
    """Retrieve available ElevenLabs and Neural voices."""
    eleven_voices = list_elevenlabs_voices()
    return {
        "engine": "elevenlabs" if eleven_client else "edge_tts",
        "elevenlabs_available": bool(eleven_client),
        "voices": eleven_voices
    }

@router.get("/speak")
async def speak(
    text: str = Query(..., description="Text to synthesize"),
    lang: str = Query("lo", description="Language: 'lo', 'hmn', 'th', 'en'"),
    gender: str = Query("male", description="'male' or 'female'"),
    voice_id: Optional[str] = Query(None, description="ElevenLabs voice ID"),
    engine: str = Query("elevenlabs", description="'elevenlabs' or 'edge_tts'")
):
    """
    Directly streams synthesized MP3 audio for HTML5 audio elements.
    """
    if not text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")

    audio_bytes, _ = await generate_speech_audio_async(
        text=text,
        lang=lang,
        gender=gender,
        voice_id=voice_id,
        engine=engine
    )

    if not audio_bytes:
        raise HTTPException(status_code=500, detail="Failed to synthesize speech audio")

    return Response(
        content=audio_bytes,
        media_type="audio/mpeg",
        headers={
            "Accept-Ranges": "bytes",
            "Content-Length": str(len(audio_bytes)),
            "Access-Control-Allow-Origin": "*",
            "Cache-Control": "public, max-age=86400"
        }
    )

@router.post("/synthesize")
async def synthesize_detailed(payload: SynthesizePayload):
    """
    Returns audio as base64 and exact word timestamps for synchronized karaoke highlighting.
    """
    if not payload.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")

    audio_bytes, word_timestamps = await generate_speech_audio_async(
        text=payload.text,
        lang=payload.lang,
        gender=payload.gender,
        voice_id=payload.voice_id,
        engine=payload.engine
    )

    if not audio_bytes:
        raise HTTPException(status_code=500, detail="Speech generation failed")

    # Calculate duration
    duration = 0.0
    if word_timestamps:
        duration = word_timestamps[-1].get("end", 0.0)

    audio_b64 = base64.b64encode(audio_bytes).decode("utf-8")

    return {
        "audio_base64": f"data:audio/mp3;base64,{audio_b64}",
        "duration": duration,
        "word_timestamps": word_timestamps,
        "words_count": len(word_timestamps)
    }

@router.post("/clone-voice")
async def clone_voice(
    name: str = Form(..., description="Name for the cloned voice"),
    description: Optional[str] = Form("Custom Cloned Voice"),
    audio_file: UploadFile = File(..., description="Voice sample (MP3, WAV, M4A)")
):
    """
    Instant Voice Cloning: Upload 1-2 minutes of audio to clone a Hmong or Lao voice in ElevenLabs!
    """
    if not eleven_client:
        raise HTTPException(status_code=400, detail="ElevenLabs API key is not configured")

    try:
        # Save temp file
        temp_path = UPLOAD_DIR / f"temp_voice_{uuid.uuid4().hex}_{audio_file.filename}"
        content = await audio_file.read()
        temp_path.write_bytes(content)

        # Clone using ElevenLabs SDK
        voice = eleven_client.clone(
            name=name,
            description=description,
            files=[str(temp_path)]
        )

        # Clean up
        if temp_path.exists():
            temp_path.unlink()

        return {
            "success": True,
            "voice_id": voice.voice_id,
            "name": voice.name,
            "message": f"Successfully cloned voice '{name}'!"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Voice cloning failed: {str(e)}")

@router.post("/save-video")
async def save_video(
    video: UploadFile = File(...),
    title: str = Form("Episode Video")
):
    """Saves exported episode video webm/mp4 to backend uploads directory."""
    try:
        ext = Path(video.filename).suffix or ".webm"
        safe_name = f"episode_{uuid.uuid4().hex[:10]}{ext}"
        saved_file = PODCAST_VIDEOS_DIR / safe_name
        
        content = await video.read()
        saved_file.write_bytes(content)

        return {
            "success": True,
            "videoPath": f"/uploads/podcast_videos/{safe_name}",
            "filename": safe_name,
            "sizeBytes": len(content)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save video: {str(e)}")
