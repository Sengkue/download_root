import os
import sys
import re
import shutil
import asyncio
import subprocess
import threading
from pathlib import Path
import imageio_ffmpeg

from app.core.config import ROOT_DIR

progress_map = {}
active_jobs_map = {}

def get_ffmpeg_path() -> str:
    env_path = os.getenv("FFMPEG_PATH")
    if env_path and os.path.isfile(env_path):
        return env_path

    try:
        exe = imageio_ffmpeg.get_ffmpeg_exe()
        if exe and os.path.isfile(exe):
            return exe
    except Exception:
        pass

    static_path = ROOT_DIR / "backend" / "node_modules" / "ffmpeg-static" / "ffmpeg.exe"
    if static_path.exists():
        return str(static_path)

    which_ffmpeg = shutil.which("ffmpeg")
    if which_ffmpeg:
        return which_ffmpeg

    return "ffmpeg"

FFMPEG_BIN = get_ffmpeg_path()

def parse_time_to_seconds(val) -> float:
    if not val:
        return 0.0
    val_str = str(val).strip()
    if val_str.isdigit():
        return int(val_str) / 1_000_000
    parts = val_str.split(":")
    if len(parts) == 3:
        try:
            return float(parts[0]) * 3600 + float(parts[1]) * 60 + float(parts[2])
        except ValueError:
            return 0.0
    try:
        return float(val_str)
    except ValueError:
        return 0.0

def escape_drawtext(text: str) -> str:
    if not text:
        return ""
    return (
        text.replace("\\", "\\\\")
            .replace(":", "\\:")
            .replace("'", "’")
            .replace(";", "\\;")
            .replace("%", "%%")
            .replace(",", "\\,")
    )

def _sync_probe_duration(file_path: str) -> float:
    if not file_path or not os.path.exists(file_path):
        return 0.0
    try:
        creationflags = 0
        if sys.platform == "win32":
            creationflags = subprocess.CREATE_NO_WINDOW if hasattr(subprocess, "CREATE_NO_WINDOW") else 0x08000000

        res = subprocess.run(
            [FFMPEG_BIN, "-i", file_path, "-hide_banner", "-f", "null", "-"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="ignore",
            check=False,
            creationflags=creationflags
        )
        match = re.search(r"Duration:\s*(\d{2}:\d{2}:\d{2}(?:\.\d+)?)", res.stderr, re.IGNORECASE)
        if match:
            return parse_time_to_seconds(match.group(1))
        return 0.0
    except Exception as e:
        print(f"probe_duration error for {file_path}: {e}")
        return 0.0

async def probe_audio_duration(audio_path: str) -> float:
    return await asyncio.to_thread(_sync_probe_duration, audio_path)

async def get_video_duration(file_path: str) -> float:
    dur = await asyncio.to_thread(_sync_probe_duration, file_path)
    return dur if dur > 0 else 5.0

def _sync_run_ffmpeg(
    args: list[str],
    job_id: str = None,
    expected_duration: float = 0,
    progress_offset: float = 0,
    progress_scale: float = 100
):
    cmd = [FFMPEG_BIN] + [str(a) for a in args]
    creationflags = 0
    if sys.platform == "win32":
        creationflags = subprocess.CREATE_NO_WINDOW if hasattr(subprocess, "CREATE_NO_WINDOW") else 0x08000000

    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="ignore",
        bufsize=1,
        creationflags=creationflags
    )

    if job_id:
        active_jobs_map[job_id] = proc

    stderr_lines = []
    def read_stderr():
        for line in proc.stderr:
            stderr_lines.append(line)
            if len(stderr_lines) > 60:
                stderr_lines.pop(0)

    err_thread = threading.Thread(target=read_stderr, daemon=True)
    err_thread.start()

    try:
        for line in proc.stdout:
            trimmed = line.strip()
            if trimmed.startswith("out_time_us=") and job_id and expected_duration > 0:
                try:
                    us = int(trimmed.split("=")[1])
                    if us > 0:
                        pct = (us / 1_000_000 / expected_duration) * progress_scale + progress_offset
                        pct = max(progress_offset, min(pct, progress_offset + progress_scale))
                        progress_map[job_id] = {
                            "progress": round(pct, 1),
                            "status": f"Encoding video... {round(pct)}%"
                        }
                except Exception:
                    pass

        proc.wait()
        err_thread.join(timeout=2.0)
    finally:
        if job_id:
            active_jobs_map.pop(job_id, None)

    if proc.returncode == 0:
        if job_id:
            progress_map[job_id] = {
                "progress": progress_offset + progress_scale,
                "status": f"Encoding video... {round(progress_offset + progress_scale)}%"
            }
        return True
    else:
        err_msg = "".join(stderr_lines)[-500:] if stderr_lines else "Unknown error"
        raise RuntimeError(f"FFmpeg exited with code {proc.returncode}: {err_msg}")

async def run_ffmpeg(
    args: list[str],
    job_id: str = None,
    expected_duration: float = 0,
    progress_offset: float = 0,
    progress_scale: float = 100
):
    return await asyncio.to_thread(
        _sync_run_ffmpeg,
        args,
        job_id,
        expected_duration,
        progress_offset,
        progress_scale
    )

def cancel_job(job_id: str) -> bool:
    proc = active_jobs_map.get(job_id)
    if proc:
        try:
            proc.kill()
            active_jobs_map.pop(job_id, None)
            progress_map.pop(job_id, None)
            return True
        except Exception as e:
            print(f"Error cancelling job {job_id}: {e}")
            return False
    return False
