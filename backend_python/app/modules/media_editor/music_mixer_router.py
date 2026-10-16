import os
import shutil
import uuid
import tempfile
import json
import random
from pathlib import Path
from fastapi import APIRouter, HTTPException, UploadFile, File, Form, BackgroundTasks
from fastapi.responses import FileResponse

from app.core.ffmpeg import (
    run_ffmpeg,
    probe_audio_duration,
    get_video_duration,
    progress_map
)
from app.modules.media_editor.overlays import build_overlay_filters

router = APIRouter(prefix="/music-mixer", tags=["Music Mixer"])

def cleanup_files(file_paths: list[str], job_id: str = None):
    if job_id and job_id in progress_map:
        progress_map.pop(job_id, None)
    for p in file_paths:
        try:
            if os.path.exists(p):
                os.remove(p)
        except Exception:
            pass

@router.post("/mix")
async def mix_music_video(
    background_tasks: BackgroundTasks,
    video: list[UploadFile] = File(...),
    audio: list[UploadFile] = File(...),
    logo: list[UploadFile] = File(None),
    jobId: str = Form(None),
    videoSpeed: float = Form(1.0),
    transitionDuration: float = Form(1.0),
    bgTransitionDuration: float = Form(None),
    bgImageDuration: float = Form(10.0),
    transitionTypes: str = Form(None),
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
    if not video or not audio:
        raise HTTPException(status_code=400, detail="Both video and audio files are required")

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

        # Merge / Process Audio
        now_playing_segments = []
        if len(audio) == 1:
            a_file = audio[0]
            a_suffix = Path(a_file.filename).suffix or ".mp3"
            audio_path = os.path.join(tmp_dir, f"audio-{uuid.uuid4().hex[:6]}{a_suffix}")
            with open(audio_path, "wb") as buf:
                shutil.copyfileobj(a_file.file, buf)
            tmp_files.append(audio_path)
            exact_audio_dur = await probe_audio_duration(audio_path)
            now_playing_segments.append({
                "title": Path(a_file.filename).stem if a_file.filename else "Track 1",
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
                filter_complex += f"[{i}:a]aformat=sample_rates=48000:channel_layouts=stereo[a{i}];"
                concat_inputs += f"[a{i}]"

                dur = await probe_audio_duration(p)
                now_playing_segments.append({
                    "title": Path(f.filename).stem if f.filename else f"Track {i+1}",
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

        # Process videos
        saved_video_paths = []
        is_image_flags = []
        for v in video:
            v_suffix = Path(v.filename).suffix or ".mp4"
            v_path = os.path.join(tmp_dir, f"vid-{uuid.uuid4().hex[:6]}{v_suffix}")
            with open(v_path, "wb") as buf:
                shutil.copyfileobj(v.file, buf)
            tmp_files.append(v_path)
            saved_video_paths.append(v_path)
            is_image_flags.append(v.content_type.startswith("image/") if v.content_type else False)

        speed = float(videoSpeed) if videoSpeed > 0 else 1.0
        t_dur = float(bgTransitionDuration or transitionDuration or 1.0)
        img_dur = float(bgImageDuration or 10.0)

        base_durations = []
        for i, vp in enumerate(saved_video_paths):
            if is_image_flags[i]:
                orig_d = img_dur
            else:
                orig_d = await get_video_duration(vp)
            adj_d = orig_d / speed
            base_durations.append(adj_d)

        total_base_dur = sum(base_durations)
        if len(saved_video_paths) > 1 and t_dur > 0:
            total_base_dur -= (len(saved_video_paths) - 1) * t_dur

        target_length = targetDuration if targetDuration > 0 else exact_audio_dur

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
                pass

        pts_multiplier = 1 / speed

        # Single Video
        if len(saved_video_paths) == 1:
            if jobId:
                progress_map[jobId] = {"progress": 10, "status": "Building single video loop..."}

            ffmpeg_args = ["-stream_loop", "-1", "-fflags", "+genpts", "-i", saved_video_paths[0], "-i", audio_path]
            filter_complex = f"[0:v]scale={resolution}:force_original_aspect_ratio=increase,crop={resolution},setsar=1,fps=30,setpts={pts_multiplier}*PTS,format=yuv420p[vbase]; "

            eff_dur = target_length or total_base_dur or 600
            if has_any_overlay:
                overlay = build_overlay_filters(overlay_params, eff_dur, 2)
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

        # Multi Video
        else:
            base_sequence_path = os.path.join(tmp_dir, f"basesequence-{tmp_id}.mp4")
            tmp_files.append(base_sequence_path)

            if jobId:
                progress_map[jobId] = {"progress": 5, "status": "Rendering base video transitions (Pass 1)..."}

            pass1_args = []
            filter_complex = ""

            for i, vp in enumerate(saved_video_paths):
                if is_image_flags[i]:
                    pass1_args.extend(["-loop", "1", "-t", str(img_dur), "-i", vp])
                else:
                    pass1_args.extend(["-i", vp])
                filter_complex += f"[{i}:v]scale={resolution}:force_original_aspect_ratio=increase,crop={resolution},setsar=1,fps=30,setpts={pts_multiplier}*PTS,format=yuv420p[v{i}]; "

            last_node = "[v0]"
            cur_offset = base_durations[0] - t_dur

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
                "-y", "-progress", "pipe:1",
                base_sequence_path
            ])
            await run_ffmpeg(pass1_args, job_id=jobId, expected_duration=total_base_dur, progress_offset=5, progress_scale=60)

            # Loop over audio
            if jobId:
                progress_map[jobId] = {"progress": 65, "status": "Looping sequence over audio (Pass 2)..."}

            loop_count = max(0, int(target_length // total_base_dur))
            pass2_args = ["-stream_loop", str(loop_count), "-i", base_sequence_path, "-vn", "-i", audio_path]

            fade_out_dur = 1.5
            fade_out_st = max(0, target_length - fade_out_dur)

            if has_any_overlay:
                overlay = build_overlay_filters(overlay_params, target_length, 2)
                for arg in overlay["extra_inputs"]:
                    pass2_args.append(arg)
                p2_filter = f"[0:v]null[vbase]; {overlay['filters']} [1:a]afade=t=out:st={fade_out_st}:d={fade_out_dur}[aout]"
                out_v = "[vout]"
            else:
                p2_filter = f"[1:a]afade=t=out:st={fade_out_st}:d={fade_out_dur}[aout]"
                out_v = "0:v"

            p2_script = os.path.join(tmp_dir, f"filter2-{tmp_id}.txt")
            with open(p2_script, "w", encoding="utf-8") as f:
                f.write(p2_filter.strip().rstrip(";"))
            tmp_files.append(p2_script)

            pass2_args.extend([
                "-filter_complex_script", p2_script,
                "-map", out_v, "-map", "[aout]",
                "-c:v", "libx264" if has_any_overlay else "copy",
                "-c:a", "aac", "-b:a", "192k",
                "-t", str(target_length),
                "-y", "-progress", "pipe:1",
                output_path
            ])
            if has_any_overlay:
                pass2_args.extend(["-preset", "medium", "-crf", "23", "-pix_fmt", "yuv420p"])

            await run_ffmpeg(pass2_args, job_id=jobId, expected_duration=target_length, progress_offset=65, progress_scale=30)

        if jobId:
            progress_map[jobId] = {"progress": 100, "status": "Complete"}

        for f in tmp_files:
            try:
                if os.path.exists(f):
                    os.remove(f)
            except Exception:
                pass

        background_tasks.add_task(cleanup_files, [output_path], jobId)

        stat_size = os.path.getsize(output_path)
        return FileResponse(
            output_path,
            media_type="video/mp4",
            headers={
                "Content-Disposition": 'attachment; filename="mixed_video.mp4"',
                "Content-Length": str(stat_size),
                "X-Video-Path": output_path,
                "Access-Control-Expose-Headers": "Content-Disposition, Content-Length, X-Video-Path"
            }
        )

    except Exception as e:
        print(f"Music mix failed: {e}")
        for f in tmp_files:
            try:
                if os.path.exists(f):
                    os.remove(f)
            except Exception:
                pass
        if jobId and jobId in progress_map:
            progress_map.pop(jobId, None)
        raise HTTPException(status_code=500, detail=f"Music mix failed: {str(e)}")
