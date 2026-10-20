import os
import shutil
import uuid
import tempfile
import json
import random
import traceback
from pathlib import Path
from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Query, Request, BackgroundTasks
from fastapi.responses import FileResponse
from pydantic import BaseModel

from app.core.ffmpeg import (
    run_ffmpeg,
    probe_audio_duration,
    get_video_duration,
    cancel_job,
    progress_map
)
from app.modules.media_editor.overlays import build_overlay_filters

router = APIRouter(prefix="/music-mixer", tags=["Music Mixer"])

class CancelRequest(BaseModel):
    jobId: str = None

@router.post("/cancel")
async def cancel_music_mixer_job(request: Request, data: CancelRequest = None, jobId: str = Query(None)):
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

@router.post("")
@router.post("/mix")
async def mix_music_video(
    background_tasks: BackgroundTasks,
    video: list[UploadFile] = File(...),
    audio: list[UploadFile] = File(...),
    logo: list[UploadFile] = File(None),
    jobId: str = Form(None),
    videoSpeed: float = Form(1.0),
    transitionDuration: float = Form(1.0),
    keepOriginalAudio: str = Form("false"),
    bgTransitionDuration: float = Form(None),
    bgImageDuration: float = Form(10.0),
    transitionTypes: str = Form(None),
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
    playlistColGap: str = Form(None),
    audioTrimData: str = Form(None),
    videoTrimData: str = Form(None),
    photoMotion: str = Form("alternate"),
    photoZoomIntensity: float = Form(0.15)
):
    if not video or not audio:
        raise HTTPException(status_code=400, detail="Both video/image(s) and audio files are required")

    tmp_files = []
    tmp_dir = tempfile.gettempdir()
    tmp_id = uuid.uuid4().hex[:8]
    output_path = os.path.join(tmp_dir, f"mixed-{tmp_id}.mp4")

    try:
        # Save logo
        logo_path = None
        if logo and len(logo) > 0 and logo[0].filename:
            l_suffix = Path(logo[0].filename).suffix or ".png"
            logo_path = os.path.join(tmp_dir, f"logo-{uuid.uuid4().hex[:6]}{l_suffix}")
            with open(logo_path, "wb") as buf:
                shutil.copyfileobj(logo[0].file, buf)
            tmp_files.append(logo_path)

        # Parse Trim Data
        audio_trims = []
        if audioTrimData:
            try:
                audio_trims = json.loads(audioTrimData)
            except Exception:
                pass

        video_trims = []
        if videoTrimData:
            try:
                video_trims = json.loads(videoTrimData)
            except Exception:
                pass

        # Merge / Process Audio
        now_playing_segments = []
        if len(audio) == 1:
            a_file = audio[0]
            a_suffix = Path(a_file.filename).suffix or ".mp3"
            raw_audio_path = os.path.join(tmp_dir, f"audio-raw-{uuid.uuid4().hex[:6]}{a_suffix}")
            with open(raw_audio_path, "wb") as buf:
                shutil.copyfileobj(a_file.file, buf)
            tmp_files.append(raw_audio_path)

            start_cut = 0.0
            end_cut = 0.0
            if len(audio_trims) > 0 and isinstance(audio_trims[0], dict):
                start_cut = float(audio_trims[0].get("start") or 0.0)
                end_cut = float(audio_trims[0].get("end") or 0.0)

            if start_cut > 0 or (end_cut > start_cut):
                trimmed_audio = os.path.join(tmp_dir, f"audio-trimmed-{uuid.uuid4().hex[:6]}.aac")
                tmp_files.append(trimmed_audio)
                trim_filter = f"atrim=start={start_cut}"
                if end_cut > start_cut:
                    trim_filter += f":end={end_cut}"
                trim_filter += ",asetpts=PTS-STARTPTS,aformat=sample_rates=48000:channel_layouts=stereo"
                await run_ffmpeg([
                    "-i", raw_audio_path,
                    "-filter_complex", f"[0:a]{trim_filter}[aout]",
                    "-map", "[aout]",
                    "-c:a", "aac", "-b:a", "192k",
                    "-y", trimmed_audio
                ])
                audio_path = trimmed_audio
            else:
                audio_path = raw_audio_path

            exact_audio_dur = await probe_audio_duration(audio_path)
            track_title = Path(a_file.filename).stem if a_file.filename else "Track 1"
            now_playing_segments.append({
                "title": track_title,
                "start": 0.0,
                "end": exact_audio_dur
            })
        else:
            if jobId:
                progress_map[jobId] = {"progress": 0, "status": "Merging audio tracks..."}
            merged_audio = os.path.join(tmp_dir, f"merged-audio-{tmp_id}.aac")
            tmp_files.append(merged_audio)

            audio_args = []
            filter_complex = ""
            concat_inputs = ""
            current_time = 0.0

            for i, f in enumerate(audio):
                a_suffix = Path(f.filename).suffix or ".mp3"
                p = os.path.join(tmp_dir, f"audio-{i}-{uuid.uuid4().hex[:6]}{a_suffix}")
                with open(p, "wb") as buf:
                    shutil.copyfileobj(f.file, buf)
                tmp_files.append(p)

                audio_args.extend(["-i", p])
                
                start_cut = 0.0
                end_cut = 0.0
                if i < len(audio_trims) and isinstance(audio_trims[i], dict):
                    start_cut = float(audio_trims[i].get("start") or 0.0)
                    end_cut = float(audio_trims[i].get("end") or 0.0)

                trim_f = ""
                if start_cut > 0 or (end_cut > start_cut):
                    trim_f = f"atrim=start={start_cut}"
                    if end_cut > start_cut:
                        trim_f += f":end={end_cut}"
                    trim_f += ",asetpts=PTS-STARTPTS,"

                filter_complex += f"[{i}:a]{trim_f}aformat=sample_rates=48000:channel_layouts=stereo[a{i}];"
                concat_inputs += f"[a{i}]"

                dur = await probe_audio_duration(p)
                if start_cut > 0:
                    dur = max(0.1, dur - start_cut)
                if end_cut > start_cut:
                    dur = min(dur, end_cut - start_cut)

                track_title = Path(f.filename).stem if f.filename else f"Track {i+1}"
                now_playing_segments.append({
                    "title": track_title,
                    "start": current_time,
                    "end": current_time + dur
                })
                current_time += dur

            exact_audio_dur = current_time
            filter_complex += f"{concat_inputs}concat=n={len(audio)}:v=0:a=1[aout]"
            audio_args.extend([
                "-filter_complex", filter_complex,
                "-map", "[aout]",
                "-c:a", "aac", "-b:a", "192k",
                "-y", merged_audio
            ])
            await run_ffmpeg(audio_args)
            audio_path = merged_audio

        # Process background media (videos or images)
        saved_video_paths = []
        is_image_flags = []
        for v in video:
            v_suffix = Path(v.filename).suffix or ".mp4"
            v_path = os.path.join(tmp_dir, f"vid-{uuid.uuid4().hex[:6]}{v_suffix}")
            with open(v_path, "wb") as buf:
                shutil.copyfileobj(v.file, buf)
            tmp_files.append(v_path)
            saved_video_paths.append(v_path)

            is_img = (v.content_type and v.content_type.startswith("image/")) or (v_suffix.lower() in [".jpg", ".jpeg", ".png", ".webp", ".bmp"])
            is_image_flags.append(is_img)

        speed = float(videoSpeed) if videoSpeed > 0 else 1.0
        t_dur = float(bgTransitionDuration if bgTransitionDuration is not None else (transitionDuration or 1.0))
        img_dur = float(bgImageDuration or 10.0)

        base_durations = []
        for i, vp in enumerate(saved_video_paths):
            if is_image_flags[i]:
                orig_d = img_dur
            else:
                orig_d = await get_video_duration(vp)
                v_start = 0.0
                v_end = 0.0
                if i < len(video_trims) and isinstance(video_trims[i], dict):
                    v_start = float(video_trims[i].get("start") or 0.0)
                    v_end = float(video_trims[i].get("end") or 0.0)
                if v_start > 0:
                    orig_d = max(0.5, orig_d - v_start)
                if v_end > v_start:
                    orig_d = min(orig_d, v_end - v_start)
            adj_d = orig_d / speed if speed > 0 else orig_d
            base_durations.append(adj_d)

        total_base_dur = sum(base_durations)
        if len(saved_video_paths) > 1 and t_dur > 0:
            total_base_dur -= (len(saved_video_paths) - 1) * t_dur

        target_length = targetDuration if targetDuration > 0 else exact_audio_dur
        quotes_input = overlayQuotesCustom or overlayCustomQuotes

        overlay_params = {
            "resolution": resolution,
            "timerEnabled": overlayTimerEnabled == "true",
            "timerMode": overlayTimerMode or "persong",
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
        has_any_overlay = (
            overlay_params["timerEnabled"] or
            (overlay_params["logoEnabled"] and logo_path) or
            overlay_params["quotesEnabled"] or
            overlay_params["showNowPlaying"]
        )

        all_transitions = ["fade", "wipeleft", "wiperight", "circlecrop", "hblur"]
        parsed_transitions = all_transitions
        if transitionTypes:
            try:
                p_trans = json.loads(transitionTypes)
                if isinstance(p_trans, list) and p_trans:
                    parsed_transitions = p_trans
            except Exception:
                parts = [t.strip() for t in transitionTypes.split(",") if t.strip()]
                if parts:
                    parsed_transitions = parts

        try:
            res_parts = resolution.replace("x", ":").split(":")
            res_w = int(res_parts[0])
            res_h = int(res_parts[1])
        except Exception:
            res_w, res_h = 1280, 720

        motion_mode = (photoMotion or "alternate").lower().strip()
        try:
            zoom_amount = max(0.05, min(0.50, float(photoZoomIntensity)))
        except Exception:
            zoom_amount = 0.15

        def get_smooth_zoompan(dir_val: str, duration_frames: int, z_amount: float, out_w: int, out_h: int) -> str:
            canvas_w = max(1920, out_w)
            canvas_h = max(1080, out_h)
            center_expr = "x='(iw-iw/zoom)/2':y='(ih-ih/zoom)/2'"
            if dir_val == "none":
                return f"zoompan=z='1':d={duration_frames}:fps=30:s={canvas_w}x{canvas_h}"
            elif dir_val == "out":
                return f"zoompan=z='if(lte(on,1),1+{z_amount},1+{z_amount}*(1-on/{duration_frames}))':{center_expr}:d={duration_frames}:fps=30:s={canvas_w}x{canvas_h}"
            else:  # "in"
                return f"zoompan=z='if(lte(on,1),1,1+{z_amount}*on/{duration_frames})':{center_expr}:d={duration_frames}:fps=30:s={canvas_w}x{canvas_h}"

        pts_multiplier = 1 / speed if speed > 0 else 1.0

        # ─── Single Video or Single Image ───
        if len(saved_video_paths) == 1:
            if jobId:
                progress_map[jobId] = {"progress": 10, "status": "Building single background loop..."}

            single_path = saved_video_paths[0]
            if is_image_flags[0]:
                eff_dur = target_length or total_base_dur or 600
                loop_frames = max(30, int(eff_dur * 30))
                ffmpeg_args = ["-loop", "1", "-i", single_path, "-i", audio_path]
                if motion_mode != "none":
                    z_dir = "in" if motion_mode in ["in", "alternate"] else "out"
                    zp = get_smooth_zoompan(z_dir, loop_frames, zoom_amount, res_w, res_h)
                    filter_complex = f"[0:v]{zp},scale={res_w}:{res_h}:force_original_aspect_ratio=increase,crop={res_w}:{res_h},setsar=1,fps=30,format=yuv420p[vbase]; "
                else:
                    filter_complex = f"[0:v]scale={resolution}:force_original_aspect_ratio=increase,crop={resolution},setsar=1,setpts={pts_multiplier}*PTS,fps=30,format=yuv420p[vbase]; "
            else:
                v_start = 0.0
                v_end = 0.0
                if len(video_trims) > 0 and isinstance(video_trims[0], dict):
                    v_start = float(video_trims[0].get("start") or 0.0)
                    v_end = float(video_trims[0].get("end") or 0.0)
                if v_start > 0 or (v_end > v_start):
                    cut_args = ["-ss", str(v_start), "-i", single_path]
                    if v_end > v_start:
                        cut_args.extend(["-to", str(v_end)])
                    trimmed_v = os.path.join(tmp_dir, f"vid-trimmed-{uuid.uuid4().hex[:6]}.mp4")
                    tmp_files.append(trimmed_v)
                    cut_args.extend(["-c", "copy", "-y", trimmed_v])
                    await run_ffmpeg(cut_args)
                    single_path = trimmed_v

                ffmpeg_args = ["-stream_loop", "-1", "-fflags", "+genpts", "-i", single_path, "-i", audio_path]
                filter_complex = f"[0:v]scale={resolution}:force_original_aspect_ratio=increase,crop={resolution},setsar=1,setpts={pts_multiplier}*PTS,fps=30,format=yuv420p[vbase]; "

            eff_dur = target_length or total_base_dur or 600
            if has_any_overlay:
                overlay = build_overlay_filters(overlay_params, eff_dur, 2, tmp_dir=tmp_dir, tmp_files=tmp_files)
                filter_complex += overlay["filters"] + " "
                for arg in overlay["extra_inputs"]:
                    ffmpeg_args.append(arg)
                out_v = "[vout]"
            else:
                out_v = "[vbase]"

            fade_out_dur = 1.5
            fade_out_st = max(0, target_length - fade_out_dur)
            filter_complex += f"[1:a]afade=t=out:st={fade_out_st}:d={fade_out_dur}[aout]"

            f_script = os.path.join(tmp_dir, f"filter-{tmp_id}.txt")
            with open(f_script, "w", encoding="utf-8") as f:
                f.write(filter_complex.strip().rstrip(";"))
            tmp_files.append(f_script)

            ffmpeg_args.extend([
                "-filter_complex_script", f_script,
                "-map", out_v, "-map", "[aout]",
                "-c:v", "libx264", "-preset", "medium", "-crf", "23", "-pix_fmt", "yuv420p",
                "-c:a", "aac", "-b:a", "192k",
                "-t", str(target_length),
                "-y", "-progress", "pipe:1",
                output_path
            ])
            await run_ffmpeg(ffmpeg_args, job_id=jobId, expected_duration=target_length, progress_offset=10, progress_scale=89)

        # ─── Multi Video / Multi Image ───
        else:
            base_sequence_path = os.path.join(tmp_dir, f"basesequence-{tmp_id}.mp4")
            tmp_files.append(base_sequence_path)

            if jobId:
                progress_map[jobId] = {"progress": 5, "status": "Rendering base video transitions (Pass 1)..."}

            pass1_args = []
            filter_complex = ""
            img_counter = 0

            for i, vp in enumerate(saved_video_paths):
                if is_image_flags[i]:
                    clip_dur = base_durations[i] + 1.0
                    frames = max(30, int(base_durations[i] * 30))
                    pass1_args.extend(["-loop", "1", "-t", str(clip_dur), "-i", vp])
                    if motion_mode != "none":
                        if motion_mode == "alternate":
                            direction = "in" if img_counter % 2 == 0 else "out"
                        else:
                            direction = motion_mode
                        img_counter += 1

                        zp = get_smooth_zoompan(direction, frames, zoom_amount, res_w, res_h)
                        filter_complex += f"[{i}:v]{zp},scale={res_w}:{res_h}:force_original_aspect_ratio=increase,crop={res_w}:{res_h},setsar=1,fps=30,format=yuv420p[v{i}]; "
                    else:
                        filter_complex += f"[{i}:v]scale={resolution}:force_original_aspect_ratio=increase,crop={resolution},setsar=1,setpts={pts_multiplier}*PTS,fps=30,format=yuv420p[v{i}]; "
                else:
                    v_start = 0.0
                    v_end = 0.0
                    if i < len(video_trims) and isinstance(video_trims[i], dict):
                        v_start = float(video_trims[i].get("start") or 0.0)
                        v_end = float(video_trims[i].get("end") or 0.0)
                    if v_start > 0 or (v_end > v_start):
                        in_args = ["-ss", str(v_start)]
                        if v_end > v_start:
                            in_args.extend(["-to", str(v_end)])
                        in_args.extend(["-i", vp])
                        pass1_args.extend(in_args)
                    else:
                        pass1_args.extend(["-i", vp])
                    filter_complex += f"[{i}:v]scale={resolution}:force_original_aspect_ratio=increase,crop={resolution},setsar=1,setpts={pts_multiplier}*PTS,fps=30,format=yuv420p[v{i}]; "

            last_node = "[v0]"
            cur_offset = base_durations[0] - t_dur

            is_none_trans = (t_dur <= 0 or (len(parsed_transitions) == 1 and parsed_transitions[0] == "none"))
            if is_none_trans:
                concat_nodes = "".join(f"[v{i}]" for i in range(len(saved_video_paths)))
                filter_complex += f"{concat_nodes}concat=n={len(saved_video_paths)}:v=1:a=0[vout]"
            else:
                for i in range(1, len(saved_video_paths)):
                    out_node = "[vout]" if i == len(saved_video_paths) - 1 else f"[xf{i}]"
                    eff = random.choice(parsed_transitions)
                    if eff == "none":
                        eff = "fade"
                    safe_offset = max(0, cur_offset)
                    filter_complex += f"{last_node}[v{i}]xfade=transition={eff}:duration={t_dur}:offset={safe_offset}{out_node}; "
                    last_node = out_node
                    cur_offset += (base_durations[i] - t_dur)

            f_script1 = os.path.join(tmp_dir, f"filter-{tmp_id}.txt")
            with open(f_script1, "w", encoding="utf-8") as f:
                f.write(filter_complex.strip().rstrip(";"))
            tmp_files.append(f_script1)

            pass1_args.extend([
                "-filter_complex_script", f_script1,
                "-map", "[vout]",
                "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p",
                "-y", "-progress", "pipe:1", base_sequence_path
            ])
            await run_ffmpeg(pass1_args, job_id=jobId, expected_duration=total_base_dur, progress_offset=5, progress_scale=50)

            # Pass 2: Overlays and audio loop
            if jobId:
                progress_map[jobId] = {"progress": 55, "status": "Looping sequence over audio (Pass 2)..."}

            loop_count = max(0, int(target_length // total_base_dur)) if total_base_dur > 0 else 0
            pass2_args = ["-stream_loop", str(loop_count), "-i", base_sequence_path, "-stream_loop", "-1", "-vn", "-i", audio_path]

            fade_out_dur = 1.5
            fade_out_st = max(0, target_length - fade_out_dur)

            if has_any_overlay:
                overlay = build_overlay_filters(overlay_params, target_length, 2, tmp_dir=tmp_dir, tmp_files=tmp_files)
                for arg in overlay["extra_inputs"]:
                    pass2_args.append(arg)

                pass2_filter = f"[0:v]null[vbase]; {overlay['filters']} [1:a]afade=t=out:st={fade_out_st}:d={fade_out_dur}[aout]"
                f_script2 = os.path.join(tmp_dir, f"filter2-{tmp_id}.txt")
                with open(f_script2, "w", encoding="utf-8") as f:
                    f.write(pass2_filter.strip().rstrip(";"))
                tmp_files.append(f_script2)

                pass2_args.extend([
                    "-filter_complex_script", f_script2,
                    "-map", "[vout]", "-map", "[aout]",
                    "-c:v", "libx264", "-preset", "medium", "-crf", "23", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-b:a", "192k",
                    "-t", str(target_length),
                    "-y", "-progress", "pipe:1", output_path
                ])
            else:
                pass2_args.extend([
                    "-filter_complex", f"[1:a]afade=t=out:st={fade_out_st}:d={fade_out_dur}[aout]",
                    "-map", "0:v", "-map", "[aout]",
                    "-c:v", "copy",
                    "-c:a", "aac", "-b:a", "192k",
                    "-t", str(target_length),
                    "-y", "-progress", "pipe:1", output_path
                ])

            await run_ffmpeg(pass2_args, job_id=jobId, expected_duration=target_length, progress_offset=55, progress_scale=44)

        if jobId:
            progress_map[jobId] = {"progress": 100, "status": "Compilation Complete!"}

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
                "Content-Disposition": 'attachment; filename="mixed_music_video.mp4"',
                "Content-Length": str(stat_size),
                "X-Video-Path": output_path,
                "Access-Control-Expose-Headers": "Content-Disposition, Content-Length, X-Video-Path"
            }
        )

    except Exception as e:
        print(f"Music mix failed: {e}")
        traceback.print_exc()
        for f in tmp_files:
            try:
                if os.path.exists(f):
                    os.remove(f)
            except Exception:
                pass
        if jobId and jobId in progress_map:
            progress_map.pop(jobId, None)
        raise HTTPException(status_code=500, detail=f"Music mix failed: {str(e)}")
