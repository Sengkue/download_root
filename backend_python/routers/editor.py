import os
import shutil
import uuid
import tempfile
from pathlib import Path
from fastapi import APIRouter, HTTPException, UploadFile, File, Form, BackgroundTasks
from fastapi.responses import FileResponse
from pydantic import BaseModel

from config.ffmpeg_utils import (
    run_ffmpeg,
    probe_audio_duration,
    progress_map,
    active_jobs_map
)
from config.overlay_filters import build_overlay_filters

router = APIRouter(prefix="/api/editor", tags=["Media Editor"])

class CancelRequest(BaseModel):
    jobId: str

@router.post("/cancel")
def cancel_job(data: CancelRequest):
    job_id = data.jobId
    if not job_id:
        raise HTTPException(status_code=400, detail="jobId is required")

    proc = active_jobs_map.get(job_id)
    if proc:
        try:
            proc.kill()
            active_jobs_map.pop(job_id, None)
            progress_map.pop(job_id, None)
            return {"success": True, "message": "Job cancelled"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    return {"success": True, "message": "Job was not running or already finished"}

def cleanup_files(file_paths: list[str], job_id: str = None):
    if job_id and job_id in progress_map:
        progress_map.pop(job_id, None)
    for p in file_paths:
        try:
            if os.path.exists(p):
                os.remove(p)
        except Exception:
            pass

@router.post("/merge")
async def merge_media(
    background_tasks: BackgroundTasks,
    image: list[UploadFile] = File(...),
    audio: list[UploadFile] = File(...),
    logo: list[UploadFile] = File(None),
    jobId: str = Form(None),
    zoomDir: str = Form("alternate"),
    zoomSpeed: str = Form("normal"),
    imageDuration: float = Form(4.0),
    transitionTypes: str = Form(None),
    transitionDuration: float = Form(1.0),
    targetDuration: float = Form(0.0),
    resolution: str = Form("1280:720"),
    overlayTimerEnabled: str = Form("false"),
    overlayTimerMinutes: str = Form("25"),
    overlayTimerBreakMinutes: str = Form("5"),
    overlayTimerPosition: str = Form("top-right"),
    overlayTimerShowProgress: str = Form("false"),
    overlayTimerWithBreak: str = Form("false"),
    overlayLogoEnabled: str = Form("false"),
    overlayLogoPosition: str = Form("bottom-right"),
    overlayLogoOpacity: str = Form("0.7"),
    overlayLogoSize: str = Form("120"),
    overlayQuotesEnabled: str = Form("false"),
    overlayQuotesInterval: str = Form("10"),
    overlayQuotesDuration: str = Form("15"),
    overlayQuotesPosition: str = Form("bottom"),
    overlayQuotesCustom: str = Form(None),
    showNowPlaying: str = Form("false")
):
    if not image or not audio:
        raise HTTPException(status_code=400, detail="Both image(s) and audio files are required")

    tmp_files = []
    tmp_dir = tempfile.gettempdir()
    tmp_id = uuid.uuid4().hex[:8]
    output_path = os.path.join(tmp_dir, f"merged-{tmp_id}.mp4")

    try:
        # Save audio files
        saved_audio_paths = []
        for a_file in audio:
            suffix = Path(a_file.filename).suffix or ".mp3"
            a_path = os.path.join(tmp_dir, f"audio-{uuid.uuid4().hex[:6]}{suffix}")
            with open(a_path, "wb") as buf:
                shutil.copyfileobj(a_file.file, buf)
            tmp_files.append(a_path)
            saved_audio_paths.append((a_path, a_file.filename))

        # Save logo if any
        logo_path = None
        if logo and len(logo) > 0 and logo[0].filename:
            l_suffix = Path(logo[0].filename).suffix or ".png"
            logo_path = os.path.join(tmp_dir, f"logo-{uuid.uuid4().hex[:6]}{l_suffix}")
            with open(logo_path, "wb") as buf:
                shutil.copyfileobj(logo[0].file, buf)
            tmp_files.append(logo_path)

        # Merge audio tracks if multiple
        final_audio_path = saved_audio_paths[0][0]
        now_playing_segments = []

        if len(saved_audio_paths) > 1:
            if jobId:
                progress_map[jobId] = {"progress": 0, "status": "Merging audio tracks..."}
            merged_audio = os.path.join(tmp_dir, f"merged-audio-{tmp_id}.aac")
            tmp_files.append(merged_audio)

            audio_args = []
            filter_complex = ""
            concat_inputs = ""
            current_time = 0.0

            for i, (p, orig_name) in enumerate(saved_audio_paths):
                audio_args.extend(["-i", p])
                filter_complex += f"[{i}:a]aformat=sample_rates=48000:channel_layouts=stereo[a{i}];"
                concat_inputs += f"[a{i}]"

                if showNowPlaying == "true":
                    dur = await probe_audio_duration(p)
                    now_playing_segments.append({
                        "title": Path(orig_name).stem if orig_name else f"Track {i+1}",
                        "start": current_time,
                        "end": current_time + dur
                    })
                    current_time += dur

            filter_complex += f"{concat_inputs}concat=n={len(saved_audio_paths)}:v=0:a=1[aout]"
            audio_args.extend([
                "-filter_complex", filter_complex,
                "-map", "[aout]",
                "-c:a", "aac", "-b:a", "192k",
                "-y", merged_audio
            ])
            await run_ffmpeg(audio_args)
            final_audio_path = merged_audio
        else:
            if showNowPlaying == "true":
                p, orig_name = saved_audio_paths[0]
                dur = await probe_audio_duration(p)
                now_playing_segments.append({
                    "title": Path(orig_name).stem if orig_name else "Track 1",
                    "start": 0.0,
                    "end": dur
                })

        # Save image files
        saved_image_paths = []
        for img in image:
            i_suffix = Path(img.filename).suffix or ".jpg"
            i_path = os.path.join(tmp_dir, f"img-{uuid.uuid4().hex[:6]}{i_suffix}")
            with open(i_path, "wb") as buf:
                shutil.copyfileobj(img.file, buf)
            tmp_files.append(i_path)
            saved_image_paths.append(i_path)

        if jobId:
            progress_map[jobId] = {"progress": 0, "status": "Analyzing audio track..."}
        audio_duration = await probe_audio_duration(final_audio_path)
        if audio_duration <= 0:
            audio_duration = 10.0

        target_length = targetDuration if targetDuration > 0 else audio_duration

        # Zoom settings
        fps = 30
        zoom_range = 0.3
        if zoomSpeed:
            try:
                zoom_range = max(0.01, min(float(zoomSpeed) / 100.0, 1.5))
            except ValueError:
                zoom_map = {"slow": 0.15, "normal": 0.3, "fast": 0.5}
                zoom_range = zoom_map.get(zoomSpeed, 0.3)

        zp_w, zp_h = 8192, 4608
        center_expr = "x='iw/2-(iw/zoom)/2':y='ih/2-(ih/zoom)/2'"

        def get_zoompan(dir_val: str, duration_frames: int) -> str:
            if dir_val == "none":
                return f"zoompan=z='1':d={duration_frames}:fps={fps}:s={zp_w}x{zp_h}"
            elif dir_val == "out":
                return f"zoompan=z='if(lte(on,1),1+{zoom_range},1+{zoom_range}*(1-on/{duration_frames}))':{center_expr}:d={duration_frames}:fps={fps}:s={zp_w}x{zp_h}"
            else:
                return f"zoompan=z='if(lte(on,1),1,1+{zoom_range}*on/{duration_frames})':{center_expr}:d={duration_frames}:fps={fps}:s={zp_w}x{zp_h}"

        overlay_params = {
            "timerEnabled": overlayTimerEnabled == "true",
            "timerMinutes": overlayTimerMinutes,
            "timerBreakMinutes": overlayTimerBreakMinutes,
            "timerPosition": overlayTimerPosition,
            "timerShowProgress": overlayTimerShowProgress == "true",
            "timerWithBreak": overlayTimerWithBreak == "true",
            "logoEnabled": overlayLogoEnabled == "true",
            "logoPath": logo_path,
            "logoPosition": overlayLogoPosition,
            "logoOpacity": overlayLogoOpacity,
            "logoSize": overlayLogoSize,
            "quotesEnabled": overlayQuotesEnabled == "true",
            "quotesInterval": overlayQuotesInterval,
            "quotesDuration": overlayQuotesDuration,
            "quotesPosition": overlayQuotesPosition,
            "customQuotes": overlayQuotesCustom,
            "showNowPlaying": showNowPlaying == "true",
            "nowPlayingSegments": now_playing_segments
        }

        has_overlays = (
            overlay_params["timerEnabled"] or
            (overlay_params["logoEnabled"] and logo_path) or
            overlay_params["quotesEnabled"] or
            overlay_params["showNowPlaying"]
        )

        res_w, res_h = resolution.split(":") if ":" in resolution else ("1280", "720")

        # ─── Case 1: Single Image ───
        if len(saved_image_paths) == 1:
            if jobId:
                progress_map[jobId] = {"progress": 10, "status": "Generating video from image..."}

            single_image = saved_image_paths[0]
            loop_frames = max(1, int(target_length * fps))
            zp_filter = get_zoompan(zoomDir if zoomDir != "alternate" else "in", loop_frames)

            filter_complex = (
                f"[0:v]{zp_filter},scale={res_w}:{res_h}:force_original_aspect_ratio=decrease,"
                f"pad={res_w}:{res_h}:(ow-iw)/2:(oh-ih)/2,format=yuv420p[vbase]; "
            )

            fade_out_st = max(0, target_length - 2)
            filter_complex += f"[1:a]afade=t=out:st={fade_out_st}:d=2[aout_final]; "

            pass_args = ["-loop", "1", "-i", single_image, "-i", final_audio_path]

            if has_overlays:
                overlay = build_overlay_filters(overlay_params, target_length, 2)
                filter_complex += overlay["filters"]
                pass_args.extend(overlay["extra_inputs"])
                out_v = "[vout]"
            else:
                out_v = "[vbase]"

            filter_script = os.path.join(tmp_dir, f"filter-{tmp_id}.txt")
            with open(filter_script, "w", encoding="utf-8") as f:
                f.write(filter_complex.strip().rstrip(";"))
            tmp_files.append(filter_script)

            pass_args.extend([
                "-filter_complex_script", filter_script,
                "-map", out_v, "-map", "[aout_final]",
                "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", str(fps),
                "-crf", "20", "-preset", "veryfast",
                "-c:a", "aac", "-b:a", "192k",
                "-t", str(target_length),
                "-y", "-progress", "pipe:1",
                output_path
            ])

            await run_ffmpeg(pass_args, job_id=jobId, expected_duration=target_length, progress_offset=10, progress_scale=89)

        # ─── Case 2: Multi-Image Slideshow ───
        else:
            if jobId:
                progress_map[jobId] = {"progress": 2, "status": "Building Ken Burns slideshow..."}

            num_images = len(saved_image_paths)
            dur_per_img = float(imageDuration)
            t_dur = float(transitionDuration)
            img_frames = int(dur_per_img * fps)

            # Pass 1: Build slideshow
            slideshow_path = os.path.join(tmp_dir, f"slideshow-{tmp_id}.mp4")
            tmp_files.append(slideshow_path)

            pass1_args = []
            filter_complex = ""

            for i, ipath in enumerate(saved_image_paths):
                pass1_args.extend(["-loop", "1", "-t", str(dur_per_img), "-i", ipath])
                if zoomDir == "alternate":
                    z_dir = "in" if i % 2 == 0 else "out"
                else:
                    z_dir = zoomDir

                zp_filter = get_zoompan(z_dir, img_frames)
                filter_complex += (
                    f"[{i}:v]{zp_filter},scale={res_w}:{res_h}:force_original_aspect_ratio=decrease,"
                    f"pad={res_w}:{res_h}:(ow-iw)/2:(oh-ih)/2,format=yuv420p[v{i}]; "
                )

            # Transitions
            trans_list = ["fade", "wipeleft", "wiperight", "circlecrop", "hblur"]
            if transitionTypes:
                try:
                    import json
                    parsed_tt = json.loads(transitionTypes)
                    if isinstance(parsed_tt, list) and parsed_tt:
                        trans_list = parsed_tt
                except Exception:
                    trans_list = [t.strip() for t in transitionTypes.split(",") if t.strip()] or trans_list

            slideshow_duration = num_images * dur_per_img - (num_images - 1) * t_dur

            last_node = "[v0]"
            cur_offset = dur_per_img - t_dur

            for i in range(1, num_images):
                effect = trans_list[(i - 1) % len(trans_list)]
                is_last = (i == num_images - 1)
                out_node = "[vout]" if is_last else f"[vtrans{i}]"
                safe_offset = max(0, cur_offset)
                filter_complex += f"{last_node}[v{i}]xfade=transition={effect}:duration={t_dur}:offset={safe_offset}{out_node}; "
                last_node = out_node
                cur_offset += (dur_per_img - t_dur)

            pass1_args.extend([
                "-filter_complex", filter_complex,
                "-map", "[vout]",
                "-c:v", "libx264", "-pix_fmt", "yuv420p",
                "-r", str(fps), "-crf", "20", "-preset", "veryfast",
                "-y", "-progress", "pipe:1",
                slideshow_path
            ])

            await run_ffmpeg(pass1_args, job_id=jobId, expected_duration=slideshow_duration, progress_offset=2, progress_scale=60)

            # Pass 2: Loop slideshow over audio duration
            if jobId:
                progress_map[jobId] = {"progress": 65, "status": "Looping slideshow over audio..."}

            loop_count = max(0, int(target_length // slideshow_duration))
            pass2_args = ["-stream_loop", str(loop_count), "-i", slideshow_path]
            if targetDuration > 0:
                pass2_args = ["-stream_loop", "-1", "-i", slideshow_path]

            fade_out_st = max(0, target_length - 2)
            pass2_args.extend(["-i", final_audio_path])

            p2_filter = f"[1:a]afade=t=out:st={fade_out_st}:d=2[aout_final]; "

            if has_overlays:
                overlay = build_overlay_filters(overlay_params, target_length, 2)
                p2_filter += f"[0:v]null[vbase]; {overlay['filters']}"
                pass2_args.extend(overlay["extra_inputs"])
                out_v = "[vout]"
            else:
                out_v = "0:v"

            p2_script = os.path.join(tmp_dir, f"filter2-{tmp_id}.txt")
            with open(p2_script, "w", encoding="utf-8") as f:
                f.write(p2_filter.strip().rstrip(";"))
            tmp_files.append(p2_script)

            if has_overlays:
                pass2_args.extend([
                    "-filter_complex_script", p2_script,
                    "-map", out_v, "-map", "[aout_final]",
                    "-c:v", "libx264", "-preset", "veryfast",
                    "-c:a", "aac", "-b:a", "192k",
                    "-t", str(target_length),
                    "-y", "-progress", "pipe:1",
                    output_path
                ])
            else:
                pass2_args.extend([
                    "-filter_complex_script", p2_script,
                    "-map", out_v, "-map", "[aout_final]",
                    "-c:v", "copy",
                    "-c:a", "aac", "-b:a", "192k",
                    "-t", str(target_length),
                    "-y", "-progress", "pipe:1",
                    output_path
                ])

            await run_ffmpeg(pass2_args, job_id=jobId, expected_duration=target_length, progress_offset=65, progress_scale=34)

        if jobId:
            progress_map[jobId] = {"progress": 100, "status": "Video ready!"}

        # Clean temporary inputs
        for f in tmp_files:
            try:
                if os.path.exists(f):
                    os.remove(f)
            except Exception:
                pass

        # Cleanup output_path after download finishes
        background_tasks.add_task(cleanup_files, [output_path], jobId)

        stat_size = os.path.getsize(output_path)
        return FileResponse(
            output_path,
            media_type="video/mp4",
            headers={
                "Content-Disposition": 'attachment; filename="generated-slideshow.mp4"',
                "Content-Length": str(stat_size),
                "X-Video-Path": output_path,
                "Access-Control-Expose-Headers": "Content-Disposition, Content-Length, X-Video-Path"
            }
        )

    except Exception as e:
        print(f"Editor merge error: {e}")
        for f in tmp_files:
            try:
                if os.path.exists(f):
                    os.remove(f)
            except Exception:
                pass
        if jobId and jobId in progress_map:
            progress_map.pop(jobId, None)
        raise HTTPException(status_code=500, detail=str(e))
