import os
import shutil
import uuid
import tempfile
import json
import traceback
from pathlib import Path
from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Query, Request, BackgroundTasks
from fastapi.responses import FileResponse
from pydantic import BaseModel

from app.core.ffmpeg import run_ffmpeg, probe_audio_duration, cancel_job, progress_map
from app.modules.media_editor.overlays import build_overlay_filters

router = APIRouter(prefix="/editor", tags=["Media Editor"])

class CancelRequest(BaseModel):
    jobId: str = None

@router.post("/cancel")
async def cancel_editor_job(request: Request, data: CancelRequest = None, jobId: str = Query(None)):
    jid = data.jobId if (data and data.jobId) else jobId
    if not jid:
        try:
            body = await request.json()
            jid = body.get("jobId")
        except Exception:
            pass
    if not jid:
        try:
            form = await request.form()
            jid = form.get("jobId")
        except Exception:
            pass

    if not jid:
        raise HTTPException(status_code=400, detail="jobId is required")
    cancel_job(jid)
    return {"success": True, "message": "Job cancelled"}

def cleanup_files(file_paths: list[str] = None, job_id: str = None):
    if job_id and job_id in progress_map:
        progress_map.pop(job_id, None)
    if file_paths:
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
    overlayTimerMode: str = Form("pomodoro"),
    overlayTimerMinutes: str = Form("25"),
    overlayTimerBreakMinutes: str = Form("5"),
    overlayTimerPosition: str = Form("top-right"),
    overlayTimerShowProgress: str = Form("false"),
    overlayTimerWithBreak: str = Form("false"),
    timerPosX: str = Form(None),
    timerPosY: str = Form(None),
    timerFontSize: str = Form(None),
    overlayLogoEnabled: str = Form("false"),
    overlayLogoPosition: str = Form("bottom-right"),
    overlayLogoOpacity: str = Form("0.7"),
    overlayLogoSize: str = Form("120"),
    overlayQuotesEnabled: str = Form("false"),
    overlayQuotesInterval: str = Form("10"),
    overlayQuotesDuration: str = Form("15"),
    overlayQuotesPosition: str = Form("bottom"),
    overlayQuotesCustom: str = Form(None),
    overlayCustomQuotes: str = Form(None),
    showNowPlaying: str = Form("false"),
    playlistPosX: str = Form(None),
    playlistPosY: str = Form(None),
    playlistFontSize: str = Form(None),
    playlistItemsPerCol: str = Form(None),
    playlistColGap: str = Form(None)
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

        # Save logo
        logo_path = None
        if logo and len(logo) > 0 and logo[0].filename:
            l_suffix = Path(logo[0].filename).suffix or ".png"
            logo_path = os.path.join(tmp_dir, f"logo-{uuid.uuid4().hex[:6]}{l_suffix}")
            with open(logo_path, "wb") as buf:
                shutil.copyfileobj(logo[0].file, buf)
            tmp_files.append(logo_path)

        final_audio_path = saved_audio_paths[0][0]
        now_playing_segments = []

        # Merge multiple audios if needed
        if len(saved_audio_paths) > 1:
            if jobId:
                progress_map[jobId] = {"progress": 1, "status": "Merging audio tracks..."}
            merged_audio_path = os.path.join(tmp_dir, f"merged_audio-{tmp_id}.aac")
            tmp_files.append(merged_audio_path)

            audio_inputs = []
            filter_complex = ""
            current_time = 0.0

            for idx, (p, orig_name) in enumerate(saved_audio_paths):
                audio_inputs.extend(["-i", p])
                filter_complex += f"[{idx}:a]aformat=sample_rates=48000:channel_layouts=stereo[a{idx}];"
                dur = await probe_audio_duration(p)
                now_playing_segments.append({
                    "title": Path(orig_name).stem if orig_name else f"Track {idx+1}",
                    "start": current_time,
                    "end": current_time + dur
                })
                current_time += dur

            filter_complex += "".join(f"[a{i}]" for i in range(len(saved_audio_paths)))
            filter_complex += f"concat=n={len(saved_audio_paths)}:v=0:a=1[outa]"

            merge_args = audio_inputs + [
                "-filter_complex", filter_complex,
                "-map", "[outa]",
                "-c:a", "aac", "-b:a", "192k",
                "-y", merged_audio_path
            ]
            await run_ffmpeg(merge_args)
            final_audio_path = merged_audio_path
        else:
            p, orig_name = saved_audio_paths[0]
            dur = await probe_audio_duration(p)
            now_playing_segments.append({
                "title": Path(orig_name).stem if orig_name else "Track 1",
                "start": 0.0,
                "end": dur
            })

        # Save images
        saved_image_paths = []
        for img_file in image:
            suffix = Path(img_file.filename).suffix or ".jpg"
            i_path = os.path.join(tmp_dir, f"img-{uuid.uuid4().hex[:6]}{suffix}")
            with open(i_path, "wb") as buf:
                shutil.copyfileobj(img_file.file, buf)
            tmp_files.append(i_path)
            saved_image_paths.append(i_path)

        audio_duration = await probe_audio_duration(final_audio_path)
        target_length = targetDuration if targetDuration > 0 else audio_duration

        fps = 30
        zoom_range = 0.15 if zoomSpeed == "slow" else (0.45 if zoomSpeed == "fast" else 0.3)
        center_expr = "x='(iw-iw/zoom)/2':y='(ih-ih/zoom)/2'"
        zp_w, zp_h = 1920, 1080

        def get_zoompan(dir_val: str, duration_frames: int) -> str:
            if dir_val == "none":
                return f"zoompan=z='1':d={duration_frames}:fps={fps}:s={zp_w}x{zp_h}"
            elif dir_val == "out":
                return f"zoompan=z='if(lte(on,1),1+{zoom_range},1+{zoom_range}*(1-on/{duration_frames}))':{center_expr}:d={duration_frames}:fps={fps}:s={zp_w}x{zp_h}"
            else:
                return f"zoompan=z='if(lte(on,1),1,1+{zoom_range}*on/{duration_frames})':{center_expr}:d={duration_frames}:fps={fps}:s={zp_w}x{zp_h}"

        quotes_input = overlayQuotesCustom or overlayCustomQuotes

        overlay_params = {
            "resolution": resolution,
            "timerEnabled": overlayTimerEnabled == "true",
            "timerMode": overlayTimerMode or "pomodoro",
            "timerMinutes": overlayTimerMinutes,
            "timerBreakMinutes": overlayTimerBreakMinutes,
            "timerPosition": overlayTimerPosition,
            "timerShowProgress": overlayTimerShowProgress == "true",
            "timerWithBreak": overlayTimerWithBreak == "true",
            "timerPosX": timerPosX,
            "timerPosY": timerPosY,
            "timerFontSize": timerFontSize,
            "logoEnabled": overlayLogoEnabled == "true",
            "logoPath": logo_path,
            "logoPosition": overlayLogoPosition,
            "logoOpacity": overlayLogoOpacity,
            "logoSize": overlayLogoSize,
            "quotesEnabled": overlayQuotesEnabled == "true",
            "quotesInterval": overlayQuotesInterval,
            "quotesDuration": overlayQuotesDuration,
            "quotesPosition": overlayQuotesPosition,
            "customQuotes": quotes_input,
            "showNowPlaying": showNowPlaying == "true",
            "nowPlayingSegments": now_playing_segments,
            "playlistPosX": playlistPosX,
            "playlistPosY": playlistPosY,
            "playlistFontSize": playlistFontSize,
            "playlistItemsPerCol": playlistItemsPerCol,
            "playlistColGap": playlistColGap
        }

        has_overlays = (
            overlay_params["timerEnabled"] or
            (overlay_params["logoEnabled"] and logo_path) or
            overlay_params["quotesEnabled"] or
            overlay_params["showNowPlaying"]
        )

        res_w, res_h = resolution.split(":") if ":" in resolution else ("1280", "720")

        # Single image
        if len(saved_image_paths) == 1:
            if jobId:
                progress_map[jobId] = {"progress": 10, "status": "Generating video from image..."}

            single_image = saved_image_paths[0]
            loop_frames = max(1, int(target_length * fps))
            zp_filter = get_zoompan(zoomDir if zoomDir != "alternate" else "in", loop_frames)

            filter_complex = (
                f"[0:v]{zp_filter},scale={res_w}:{res_h}:force_original_aspect_ratio=decrease,"
                f"pad={res_w}:{res_h}:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=30,format=yuv420p[vbase]; "
            )

            fade_out_st = max(0, target_length - 2)
            filter_complex += f"[1:a]afade=t=out:st={fade_out_st}:d={min(2.0, target_length)}[aout_final]; "

            pass_args = ["-loop", "1", "-i", single_image, "-i", final_audio_path]

            if has_overlays:
                overlay = build_overlay_filters(overlay_params, target_length, 2, tmp_dir=tmp_dir, tmp_files=tmp_files)
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

        # Multi image slideshow
        else:
            if jobId:
                progress_map[jobId] = {"progress": 2, "status": "Building Ken Burns slideshow..."}

            num_images = len(saved_image_paths)
            dur_per_img = float(imageDuration)
            t_dur = float(transitionDuration)
            img_frames = int(dur_per_img * fps)

            slideshow_path = os.path.join(tmp_dir, f"slideshow-{tmp_id}.mp4")
            tmp_files.append(slideshow_path)

            pass1_args = []
            filter_complex = ""

            for i, ipath in enumerate(saved_image_paths):
                pass1_args.extend(["-loop", "1", "-t", str(dur_per_img), "-i", ipath])
                z_dir = ("in" if i % 2 == 0 else "out") if zoomDir == "alternate" else zoomDir
                zp_filter = get_zoompan(z_dir, img_frames)
                filter_complex += (
                    f"[{i}:v]{zp_filter},scale={res_w}:{res_h}:force_original_aspect_ratio=decrease,"
                    f"pad={res_w}:{res_h}:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=30,format=yuv420p[v{i}]; "
                )

            trans_list = ["fade", "wipeleft", "wiperight", "circlecrop", "hblur"]
            if transitionTypes:
                try:
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

            f_script1 = os.path.join(tmp_dir, f"filter1-{tmp_id}.txt")
            with open(f_script1, "w", encoding="utf-8") as f:
                f.write(filter_complex.strip().rstrip(";"))
            tmp_files.append(f_script1)

            pass1_args.extend([
                "-filter_complex_script", f_script1,
                "-map", "[vout]",
                "-c:v", "libx264", "-pix_fmt", "yuv420p",
                "-r", str(fps), "-crf", "20", "-preset", "veryfast",
                "-y", "-progress", "pipe:1",
                slideshow_path
            ])

            await run_ffmpeg(pass1_args, job_id=jobId, expected_duration=slideshow_duration, progress_offset=2, progress_scale=50)

            # Pass 2: Overlays, Loop, and Audio
            if jobId:
                progress_map[jobId] = {"progress": 52, "status": "Applying overlays & audio sync..."}

            loop_count = max(0, int(target_length // slideshow_duration)) if slideshow_duration > 0 else 0
            fade_out_st = max(0, target_length - 2)

            pass2_args = ["-stream_loop", str(loop_count), "-i", slideshow_path, "-i", final_audio_path]

            if has_overlays:
                overlay = build_overlay_filters(overlay_params, target_length, 2, tmp_dir=tmp_dir, tmp_files=tmp_files)
                filter2 = f"[0:v]null[vbase]; {overlay['filters']} [1:a]afade=t=out:st={fade_out_st}:d={min(2.0, target_length)}[aout]"
                pass2_args.extend(overlay["extra_inputs"])

                f_script2 = os.path.join(tmp_dir, f"filter2-{tmp_id}.txt")
                with open(f_script2, "w", encoding="utf-8") as f:
                    f.write(filter2.strip().rstrip(";"))
                tmp_files.append(f_script2)

                pass2_args.extend([
                    "-filter_complex_script", f_script2,
                    "-map", "[vout]", "-map", "[aout]",
                    "-c:v", "libx264", "-preset", "medium", "-crf", "23", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-b:a", "192k",
                    "-t", str(target_length),
                    "-y", "-progress", "pipe:1",
                    output_path
                ])
            else:
                pass2_args.extend([
                    "-filter_complex", f"[1:a]afade=t=out:st={fade_out_st}:d={min(2.0, target_length)}[aout]",
                    "-map", "0:v", "-map", "[aout]",
                    "-c:v", "copy",
                    "-c:a", "aac", "-b:a", "192k",
                    "-t", str(target_length),
                    "-y", "-progress", "pipe:1",
                    output_path
                ])

            await run_ffmpeg(pass2_args, job_id=jobId, expected_duration=target_length, progress_offset=52, progress_scale=47)

        if jobId:
            progress_map[jobId] = {"progress": 100, "status": "Complete"}

        for f in tmp_files:
            try:
                if os.path.exists(f):
                    os.remove(f)
            except Exception:
                pass

        background_tasks.add_task(cleanup_files, [], jobId)

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
        traceback.print_exc()
        for f in tmp_files:
            try:
                if os.path.exists(f):
                    os.remove(f)
            except Exception:
                pass
        if jobId and jobId in progress_map:
            progress_map.pop(jobId, None)
        raise HTTPException(status_code=500, detail=str(e))
