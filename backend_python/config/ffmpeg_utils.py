import os
import re
import shutil
import asyncio
from pathlib import Path
import imageio_ffmpeg

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

    static_path = Path(__file__).resolve().parent.parent.parent / "backend" / "node_modules" / "ffmpeg-static" / "ffmpeg.exe"
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

async def probe_audio_duration(audio_path: str) -> float:
    try:
        proc = await asyncio.create_subprocess_exec(
            FFMPEG_BIN, "-i", audio_path, "-hide_banner", "-f", "null", "-",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        _, stderr = await proc.communicate()
        text = stderr.decode("utf-8", errors="ignore")
        match = re.search(r"Duration:\s*(\d{2}:\d{2}:\d{2}(?:\.\d+)?)", text, re.IGNORECASE)
        if match:
            return parse_time_to_seconds(match.group(1))
        return 0.0
    except Exception as e:
        print(f"probe_audio_duration error: {e}")
        return 0.0

async def get_video_duration(file_path: str) -> float:
    try:
        proc = await asyncio.create_subprocess_exec(
            FFMPEG_BIN, "-i", file_path, "-hide_banner", "-f", "null", "-",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        _, stderr = await proc.communicate()
        text = stderr.decode("utf-8", errors="ignore")
        match = re.search(r"Duration:\s*(\d{2}:\d{2}:\d{2}(?:\.\d+)?)", text, re.IGNORECASE)
        if match:
            return parse_time_to_seconds(match.group(1))
        return 5.0
    except Exception as e:
        print(f"get_video_duration error: {e}")
        return 5.0

async def run_ffmpeg(args: list[str], job_id: str = None, expected_duration: float = 0, progress_offset: float = 0, progress_scale: float = 100):
    cmd = [FFMPEG_BIN] + [str(a) for a in args]
    proc = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    if job_id:
        active_jobs_map[job_id] = proc

    async def read_stdout():
        buffer = ""
        while True:
            chunk = await proc.stdout.read(1024)
            if not chunk:
                break
            buffer += chunk.decode("utf-8", errors="ignore")
            lines = buffer.split("\n")
            buffer = lines.pop()
            for line in lines:
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

    stdout_task = asyncio.create_task(read_stdout())
    _, stderr = await proc.communicate()
    await stdout_task

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
        err_msg = stderr.decode("utf-8", errors="ignore")[-500:] if stderr else "Unknown error"
        raise RuntimeError(f"FFmpeg exited with code {proc.returncode}: {err_msg}")
