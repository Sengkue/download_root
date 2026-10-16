import os
import re
import json
import uuid
import tempfile
import asyncio
import urllib.parse
from pathlib import Path
import httpx
from fastapi import APIRouter, HTTPException, Query, BackgroundTasks
from fastapi.responses import StreamingResponse, FileResponse
import yt_dlp

from app.core.ffmpeg import progress_map, FFMPEG_BIN
from app.modules.downloader.schemas import InfoRequest, DownloadRequest

router = APIRouter(tags=["Downloader"])

def clean_target_url(url: str) -> str:
    try:
        parsed = urllib.parse.urlparse(url)
        q = urllib.parse.parse_qs(parsed.query)
        q.pop("list", None)
        q.pop("start_radio", None)
        q.pop("index", None)
        new_query = urllib.parse.urlencode(q, doseq=True)
        return urllib.parse.urlunparse(parsed._replace(query=new_query))
    except Exception:
        return url

def delete_file_safely(file_path: str, job_id: str = None):
    if job_id and job_id in progress_map:
        progress_map.pop(job_id, None)
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        print(f"Failed to delete {file_path}: {e}")

@router.get("/progress")
async def get_progress(jobId: str = Query(None)):
    if not jobId:
        raise HTTPException(status_code=400, detail="jobId is required")

    async def event_stream():
        yield f"data: {json.dumps({'progress': 0, 'status': 'Connecting...'})}\n\n"
        try:
            while True:
                job_data = progress_map.get(jobId)
                if job_data:
                    yield f"data: {json.dumps(job_data)}\n\n"
                await asyncio.sleep(0.5)
        except asyncio.CancelledError:
            pass

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive"
        }
    )

@router.post("/info")
async def get_info(data: InfoRequest):
    if not data.url:
        raise HTTPException(status_code=400, detail="URL is required.")

    clean_url = clean_target_url(data.url)

    # TikTok info check
    if "tiktok.com" in clean_url:
        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                res = await client.get(f"https://www.tikwm.com/api/?url={urllib.parse.quote(clean_url)}")
                if res.status_code == 200:
                    json_data = res.json()
                    if json_data.get("code") == 0 and json_data.get("data"):
                        d = json_data["data"]
                        return {
                            "title": d.get("title", "TikTok Video"),
                            "thumbnail": d.get("cover", ""),
                            "qualities": [1080],
                            "duration": d.get("duration", 0)
                        }
        except Exception as err:
            print(f"TikTok info fallback error: {err}")

    def run_extract():
        ydl_opts = {
            "skip_download": True,
            "no_warnings": True,
            "quiet": True,
            "noplaylist": True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            return ydl.extract_info(clean_url, download=False)

    try:
        loop = asyncio.get_event_loop()
        info = await loop.run_in_executor(None, run_extract)
        formats = info.get("formats", [])
        video_heights = [
            f.get("height") for f in formats
            if f.get("vcodec") and f.get("vcodec") != "none" and f.get("height")
        ]
        unique_heights = sorted(list(set(video_heights)), reverse=True)

        return {
            "title": info.get("title", ""),
            "thumbnail": info.get("thumbnail", ""),
            "qualities": unique_heights if unique_heights else [1080, 720, 480, 360],
            "duration": info.get("duration", 0)
        }
    except Exception as e:
        print(f"Info error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch video information: {str(e)}")

@router.post("/download")
async def download_media(data: DownloadRequest, background_tasks: BackgroundTasks):
    url = data.url
    req_type = data.type
    quality = data.quality
    job_id = data.jobId

    if not url or not req_type:
        raise HTTPException(status_code=400, detail="URL and type are required.")

    # 1. Image download
    if req_type == "image":
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Referer": "https://pixabay.com/"
        }
        client = httpx.AsyncClient(headers=headers, timeout=30.0, follow_redirects=True)
        try:
            req = client.build_request("GET", url)
            resp = await client.send(req, stream=True)
            if resp.status_code != 200:
                await client.aclose()
                raise HTTPException(status_code=400, detail="Failed to fetch image from URL.")

            url_path = urllib.parse.urlparse(url).path
            filename = url_path.split("/")[-1] or "downloaded-image.jpg"
            content_type = resp.headers.get("content-type", "application/octet-stream")
            content_length = resp.headers.get("content-length")

            async def stream_img():
                try:
                    async for chunk in resp.aiter_bytes():
                        yield chunk
                finally:
                    await resp.aclose()
                    await client.aclose()

            resp_headers = {
                "Content-Disposition": f'attachment; filename="{filename}"',
                "Access-Control-Expose-Headers": "Content-Disposition, Content-Length"
            }
            if content_length:
                resp_headers["Content-Length"] = content_length

            return StreamingResponse(stream_img(), media_type=content_type, headers=resp_headers)
        except Exception as e:
            await client.aclose()
            raise HTTPException(status_code=500, detail=str(e))

    # 2. Video / Audio download
    elif req_type in ["video", "audio"]:
        is_audio = req_type == "audio"
        ext = "mp3" if is_audio else "mp4"

        # TikTok direct stream
        if "tiktok.com" in url:
            try:
                if job_id:
                    progress_map[job_id] = {"progress": 10, "status": "Fetching TikTok info..."}

                async with httpx.AsyncClient(timeout=20.0) as client:
                    api_resp = await client.get(f"https://www.tikwm.com/api/?url={urllib.parse.quote(url)}")
                    if api_resp.status_code == 200:
                        t_data = api_resp.json()
                        if t_data.get("code") == 0 and t_data.get("data"):
                            stream_url = t_data["data"].get("music") if is_audio else (t_data["data"].get("play") or t_data["data"].get("wmplay"))
                            if stream_url:
                                if job_id:
                                    progress_map[job_id] = {"progress": 50, "status": "Downloading from TikTok..."}

                                video_client = httpx.AsyncClient(timeout=60.0, follow_redirects=True)
                                req = video_client.build_request("GET", stream_url)
                                video_resp = await video_client.send(req, stream=True)

                                content_length = video_resp.headers.get("content-length")
                                content_type = video_resp.headers.get("content-type") or ("audio/mpeg" if is_audio else "video/mp4")

                                async def stream_tiktok():
                                    try:
                                        if job_id:
                                            progress_map[job_id] = {"progress": 100, "status": "Streaming to browser..."}
                                        async for chunk in video_resp.aiter_bytes():
                                            yield chunk
                                    finally:
                                        await video_resp.aclose()
                                        await video_client.aclose()
                                        if job_id:
                                            progress_map.pop(job_id, None)

                                resp_headers = {
                                    "Content-Disposition": f'attachment; filename="tiktok-{req_type}.{ext}"',
                                    "Access-Control-Expose-Headers": "Content-Disposition, Content-Length"
                                }
                                if content_length:
                                    resp_headers["Content-Length"] = content_length

                                return StreamingResponse(stream_tiktok(), media_type=content_type, headers=resp_headers)
            except Exception as tt_err:
                print(f"TikTok direct stream error: {tt_err}")
                if job_id:
                    progress_map[job_id] = {"progress": 10, "status": "Falling back to yt-dlp..."}

        # Native yt-dlp
        clean_url = clean_target_url(url)
        tmp_id = uuid.uuid4().hex[:8]
        tmp_dir = tempfile.gettempdir()
        tmp_template = os.path.join(tmp_dir, f"yt-{tmp_id}_%(title)s.%(ext)s")

        if job_id:
            progress_map[job_id] = {"progress": 0, "status": "Starting download..."}

        def ydl_hook(d):
            if not job_id:
                return
            if d.get("status") == "downloading":
                p_str = d.get("_percent_str", "0%").strip()
                clean_p = re.sub(r"\x1b\[[0-9;]*m", "", p_str).replace("%", "")
                try:
                    pct = float(clean_p)
                    progress_map[job_id] = {"progress": pct, "status": "Downloading..."}
                except ValueError:
                    pass
            elif d.get("status") == "finished":
                progress_map[job_id] = {"progress": 99, "status": "Processing media..."}

        ydl_opts = {
            "ffmpeg_location": FFMPEG_BIN,
            "outtmpl": tmp_template,
            "noplaylist": True,
            "progress_hooks": [ydl_hook],
            "quiet": True,
            "no_warnings": True,
        }

        if is_audio:
            ydl_opts.update({
                "format": "bestaudio/best",
                "postprocessors": [{
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "0",
                }],
            })
        else:
            q_str = str(quality) if quality else None
            if q_str and q_str.isdigit():
                ydl_opts["format"] = f"bestvideo[height<={q_str}][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<={q_str}]+bestaudio/best"
            else:
                ydl_opts["format"] = "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"
            ydl_opts["merge_output_format"] = "mp4"

        def run_dl():
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([clean_url])

        try:
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, run_dl)

            matching_files = [
                os.path.join(tmp_dir, f)
                for f in os.listdir(tmp_dir)
                if f.startswith(f"yt-{tmp_id}_") and os.path.isfile(os.path.join(tmp_dir, f))
            ]

            if not matching_files:
                raise HTTPException(status_code=500, detail="yt-dlp finished but output file was not found.")

            output_file = matching_files[0]
            file_name = Path(output_file).name
            prefix_len = len(f"yt-{tmp_id}_")
            actual_filename = file_name[prefix_len:] if len(file_name) > prefix_len else f"download.{ext}"

            encoded_filename = urllib.parse.quote(actual_filename)
            content_type = "audio/mpeg" if is_audio else "video/mp4"

            background_tasks.add_task(delete_file_safely, output_file, job_id)

            return FileResponse(
                output_file,
                media_type=content_type,
                headers={
                    "Content-Disposition": f"attachment; filename*=UTF-8''{encoded_filename}",
                    "Access-Control-Expose-Headers": "Content-Disposition, Content-Length"
                }
            )
        except Exception as dl_err:
            print(f"Download execution error: {dl_err}")
            if job_id and job_id in progress_map:
                progress_map.pop(job_id, None)
            raise HTTPException(status_code=500, detail=f"Failed to download: {str(dl_err)}")
    else:
        raise HTTPException(status_code=400, detail='Invalid file type. Must be "image", "video", or "audio".')
