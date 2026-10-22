import os
import sys
import json
import time
import uuid
import ssl
import shutil
import asyncio
import subprocess
import urllib.request
from pathlib import Path
from typing import Optional, List
from datetime import datetime

import httpx
import imageio_ffmpeg
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field
from gradio_client import Client

from app.core.config import UPLOAD_DIR, API_KEYS

meta_music_router = APIRouter(prefix="/meta-music", tags=["Meta MusicGen"])
router = meta_music_router

# Meta Music Storage directory under uploads
META_MUSIC_DIR = UPLOAD_DIR / "meta_music"
META_MUSIC_DIR.mkdir(parents=True, exist_ok=True)
TRACKS_INDEX_FILE = META_MUSIC_DIR / "tracks.json"

# SSL Context for downloads
SSL_CTX = ssl.create_default_context()
SSL_CTX.check_hostname = False
SSL_CTX.verify_mode = ssl.CERT_NONE

class GenerateMusicRequest(BaseModel):
    prompt: str = Field(..., description="Music prompt description")
    duration: int = Field(15, ge=10, le=30, description="Duration in seconds (10 to 30)")
    seed: int = Field(5, ge=0, le=10, description="Seed (0 to 10)")
    title: Optional[str] = Field(None, description="Optional custom title")
    hf_token: Optional[str] = Field(None, description="Optional Hugging Face user token")

class SetTokenRequest(BaseModel):
    token: str = Field(..., description="Hugging Face User Token")

class EnhancePromptRequest(BaseModel):
    prompt: str = Field(..., description="Prompt in Lao or English to enhance")

def _load_tracks() -> List[dict]:
    if not TRACKS_INDEX_FILE.exists():
        return []
    try:
        with open(TRACKS_INDEX_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def _save_tracks(tracks: List[dict]):
    try:
        with open(TRACKS_INDEX_FILE, "w", encoding="utf-8") as f:
            json.dump(tracks, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"[MetaMusic] Error saving tracks index: {e}")

def _generate_music_worker(prompt: str, duration: int, seed: int, title: Optional[str], hf_token: Optional[str] = None) -> dict:
    track_id = f"meta_{int(time.time())}_{uuid.uuid4().hex[:6]}"
    display_title = title.strip() if title and title.strip() else f"Meta Track - {prompt[:30].strip()}..."

    temp_run_dir = META_MUSIC_DIR / f"temp_{track_id}"
    temp_run_dir.mkdir(parents=True, exist_ok=True)

    token_to_use = (hf_token or os.getenv("HF_TOKEN") or "").strip()

    try:
        print(f"[MetaMusic] Starting generation: '{prompt}' | Duration: {duration}s | Seed: {seed} | Has Token: {bool(token_to_use)}")
        
        def _call_musicgen(tok: Optional[str]):
            client_kwargs = {
                "ssl_verify": False,
                "download_files": False
            }
            if tok:
                client_kwargs["token"] = tok
            c = Client("sanchit-gandhi/musicgen-streaming", **client_kwargs)
            return c.predict(
                text_prompt=prompt,
                audio_length_in_s=float(duration),
                play_steps_in_s=2.5,
                seed=int(seed),
                api_name="/generate_audio"
            )

        res = None
        try:
            res = _call_musicgen(token_to_use if token_to_use else None)
        except Exception as e:
            err_text = str(e)
            if token_to_use and ("ZeroGPU" in err_text or "limit" in err_text.lower() or "429" in err_text):
                print(f"[MetaMusic] User Token limit reached. Automatically falling back to Anonymous Quota...")
                res = _call_musicgen(None)
            else:
                raise

        if not isinstance(res, dict) or "url" not in res:
            raise RuntimeError(f"Unexpected response from MusicGen: {res}")

        m3u8_url = res["url"]
        base_stream_url = m3u8_url.rsplit("/", 1)[0] + "/"

        # Fetch playlist content
        req = urllib.request.Request(m3u8_url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, context=SSL_CTX, timeout=30) as r:
            playlist_content = r.read().decode("utf-8")

        segments = [line.strip() for line in playlist_content.splitlines() if line.strip().endswith(".aac")]
        if not segments:
            raise RuntimeError("No audio segments found in MusicGen playlist")

        print(f"[MetaMusic] Downloading {len(segments)} audio segments...")
        local_segments = []
        for seg in segments:
            seg_local = temp_run_dir / seg
            seg_remote = base_stream_url + seg
            sreq = urllib.request.Request(seg_remote, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(sreq, context=SSL_CTX, timeout=30) as sr:
                with open(seg_local, "wb") as sf:
                    sf.write(sr.read())
            local_segments.append(seg_local)

        ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
        mp3_out = META_MUSIC_DIR / f"{track_id}.mp3"
        wav_out = META_MUSIC_DIR / f"{track_id}.wav"

        # Seamless Audio Assembly:
        # Instead of raw concat (which retains the 32ms AAC priming delay & chunk boundary jumps),
        # we chain equal-power acrossfade (qsin) across all segments to guarantee 100% gapless continuous audio.
        if len(local_segments) == 1:
            cmd_mp3 = [
                ffmpeg_exe, "-y",
                "-i", local_segments[0].as_posix(),
                "-c:a", "libmp3lame",
                "-b:a", "256k",
                mp3_out.as_posix()
            ]
            cmd_wav = [
                ffmpeg_exe, "-y",
                "-i", local_segments[0].as_posix(),
                "-c:a", "pcm_s16le",
                wav_out.as_posix()
            ]
            subprocess.run(cmd_mp3, capture_output=True, check=True)
            subprocess.run(cmd_wav, capture_output=True, check=True)
        else:
            inputs = []
            for s in local_segments:
                inputs.extend(["-i", s.as_posix()])

            filter_parts = []
            last_label = "0:a"
            for i in range(1, len(local_segments)):
                next_label = f"a{i}" if i < len(local_segments) - 1 else "aout"
                filter_parts.append(f"[{last_label}][{i}:a]acrossfade=d=0.08:c1=qsin:c2=qsin[{next_label}]")
                last_label = next_label

            filter_complex = ";".join(filter_parts)

            # Export MP3 (256k)
            cmd_mp3 = [
                ffmpeg_exe, "-y",
                *inputs,
                "-filter_complex", filter_complex,
                "-map", "[aout]",
                "-c:a", "libmp3lame",
                "-b:a", "256k",
                mp3_out.as_posix()
            ]
            sub_mp3 = subprocess.run(cmd_mp3, capture_output=True, text=True)
            if sub_mp3.returncode != 0:
                raise RuntimeError(f"FFmpeg MP3 export failed: {sub_mp3.stderr}")

            # Export WAV
            cmd_wav = [
                ffmpeg_exe, "-y",
                *inputs,
                "-filter_complex", filter_complex,
                "-map", "[aout]",
                "-c:a", "pcm_s16le",
                wav_out.as_posix()
            ]
            subprocess.run(cmd_wav, capture_output=True, text=True)

        track_data = {
            "id": track_id,
            "title": display_title,
            "prompt": prompt,
            "duration": duration,
            "seed": seed,
            "model": "facebook/musicgen-small",
            "mp3_url": f"/uploads/meta_music/{track_id}.mp3",
            "wav_url": f"/uploads/meta_music/{track_id}.wav",
            "file_size_mp3": mp3_out.stat().st_size if mp3_out.exists() else 0,
            "file_size_wav": wav_out.stat().st_size if wav_out.exists() else 0,
            "created_at": datetime.now().isoformat()
        }

        # Update index
        tracks = _load_tracks()
        tracks.insert(0, track_data)
        _save_tracks(tracks)

        print(f"[MetaMusic] Successfully generated: {track_id} ({mp3_out.stat().st_size} bytes)")
        return track_data

    finally:
        # Clean up temporary run directory
        if temp_run_dir.exists():
            shutil.rmtree(temp_run_dir, ignore_errors=True)

@router.get("/status")
async def get_status():
    return {
        "status": "online",
        "service": "Meta MusicGen Python Backend",
        "model": "facebook/musicgen-small",
        "min_duration": 10,
        "max_duration": 30,
        "output_formats": ["mp3", "wav"]
    }

@router.get("/tracks")
async def get_tracks():
    tracks = _load_tracks()
    # Filter to only existing tracks
    valid_tracks = []
    for t in tracks:
        mp3_name = Path(t.get("mp3_url", "")).name
        if mp3_name and (META_MUSIC_DIR / mp3_name).exists():
            valid_tracks.append(t)
    return {"tracks": valid_tracks, "count": len(valid_tracks)}

@router.post("/generate")
async def generate_music(req: GenerateMusicRequest):
    prompt = req.prompt.strip()
    if not prompt:
        raise HTTPException(status_code=400, detail="Prompt is required")

    duration = max(10, min(30, req.duration))
    seed = max(0, min(10, req.seed))

    try:
        # Run blocking HuggingFace / Gradio generation in background thread
        track_data = await asyncio.to_thread(_generate_music_worker, prompt, duration, seed, req.title, req.hf_token)
        return {
            "success": True,
            "track": track_data
        }
    except Exception as e:
        err_msg = str(e)
        print(f"[MetaMusic Error] {err_msg}")
        if "ZeroGPU" in err_msg or "limit" in err_msg.lower() or "429" in err_msg:
            raise HTTPException(
                status_code=429,
                detail="ZeroGPU Quota Limit Reached (ໂຄຕ້າຟຣີຂອງ Token ນີ້ໝົດແລ້ວ). ທ່ານສາມາດສ້າງ Hugging Face Token ໃໝ່ໄດ້ຟຣີ 100% ຈາກ https://huggingface.co/settings/tokens ແລ້ວນຳມາວາງໃສ່ຊ່ອງ Token ຢູ່ໜ້າເວັບເພື່ອສ້າງເພງຕໍ່ໄດ້ທັນທີ!"
            )
        raise HTTPException(status_code=500, detail=f"Music generation failed: {err_msg}")

@router.get("/token")
async def get_token_status():
    token = os.getenv("HF_TOKEN", "").strip()
    if token:
        masked = token[:4] + "..." + token[-4:] if len(token) > 8 else "***"
        return {"has_token": True, "masked_token": masked, "token": token}
    return {"has_token": False, "masked_token": "", "token": ""}

@router.post("/token")
async def save_hf_token(req: SetTokenRequest):
    token = req.token.strip()
    os.environ["HF_TOKEN"] = token
    # Save to backend_python/.env
    env_file = Path(__file__).resolve().parent.parent.parent.parent / ".env"
    if env_file.exists():
        content = env_file.read_text(encoding="utf-8")
        if "HF_TOKEN=" in content:
            lines = [f"HF_TOKEN={token}" if l.startswith("HF_TOKEN=") else l for l in content.splitlines()]
            env_file.write_text("\n".join(lines), encoding="utf-8")
        else:
            with open(env_file, "a", encoding="utf-8") as f:
                f.write(f"\nHF_TOKEN={token}\n")
    return {"success": True, "message": "Hugging Face Token saved successfully"}

@router.delete("/tracks/{track_id}")
async def delete_track(track_id: str):
    mp3_file = META_MUSIC_DIR / f"{track_id}.mp3"
    wav_file = META_MUSIC_DIR / f"{track_id}.wav"

    if mp3_file.exists():
        mp3_file.unlink()
    if wav_file.exists():
        wav_file.unlink()

    tracks = _load_tracks()
    new_tracks = [t for t in tracks if t.get("id") != track_id]
    _save_tracks(new_tracks)

    return {"success": True, "deleted": track_id}

@router.post("/enhance-prompt")
async def enhance_prompt(req: EnhancePromptRequest):
    user_prompt = req.prompt.strip()
    if not user_prompt:
        raise HTTPException(status_code=400, detail="Prompt is required")

    if not API_KEYS:
        # Fallback enhancement without Gemini
        return {
            "enhanced_prompt": f"melodic acoustic musical arrangement, {user_prompt}, warm instruments, high quality audio production"
        }

    system_instruction = (
        "You are an expert music producer and audio engineer specializing in prompt engineering for Meta MusicGen. "
        "The user will give you a musical idea, genre, or mood (often in Lao or simple English). "
        "Transform it into a rich, detailed, English text prompt for Meta MusicGen. "
        "Include specific acoustic instruments (e.g., Lao traditional khaen bamboo mouth organ, acoustic guitar, soft percussion, wooden flute), "
        "mood, tempo (e.g., 85 bpm), sonic textures, and production quality. "
        "Return ONLY the enhanced prompt string (1 to 2 sentences max). Do NOT add quotation marks or conversational commentary."
    )

    models_to_try = ["gemini-2.0-flash", "gemini-1.5-flash", "gemini-2.5-flash"]
    async with httpx.AsyncClient(timeout=15.0) as client:
        for api_key in API_KEYS:
            for model_name in models_to_try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
                payload = {
                    "contents": [{"parts": [{"text": f"Enhance this music idea for MusicGen: {user_prompt}"}]}],
                    "systemInstruction": {"parts": [{"text": system_instruction}]}
                }
                try:
                    res = await client.post(url, json=payload)
                    if res.status_code == 200:
                        data = res.json()
                        candidates = data.get("candidates", [])
                        if candidates and "content" in candidates[0]:
                            text = candidates[0]["content"]["parts"][0]["text"].strip()
                            return {"enhanced_prompt": text}
                except Exception:
                    continue

    return {
        "enhanced_prompt": f"melodic acoustic arrangement, {user_prompt}, warm tones, atmospheric melody, 85 bpm, high fidelity"
    }
