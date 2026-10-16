import os
import shutil
import uuid
import tempfile
import json
import random
from pathlib import Path
from fastapi import APIRouter, HTTPException, UploadFile, File, Form, BackgroundTasks
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

router = APIRouter(prefix="/video-mixer", tags=["Video Mixer"])

class CancelRequest(BaseModel):
    jobId: str

@router.post("/cancel")
def cancel_mixer_job(data: CancelRequest):
    if not data.jobId:
        raise HTTPException(status_code=400, detail="jobId is required")
    cancel_job(data.jobId)
    return {"success": True, "message": "Job cancelled"}

def cleanup_files(file_paths: list[str], job_id: str = None):
    if job_id and job_id in progress_map:
        progress_map.pop(job_id, None)
    for p in file_paths:
        try:
            if os.path.exists(p):
                os.remove(p)
        except Exception:
            pass

@router.post("")
async def mix_video(
    background_tasks: BackgroundTasks,
    video: list[UploadFile] = File(...),
    audio: list[UploadFile] = File(None),
    logo: list[UploadFile] = File(None),
    jobId: str = Form(None),
    videoSpeed: float = Form(1.0),
    transitionDuration: float = Form(1.0),
    transitionTypes: str = Form(None),
    keepOriginalAudio: str = Form("false"),
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
    if not video:
        raise HTTPException(status_code=400, detail="Video file is required")

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

        now_playing_segments = []
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

        # Save audio
        audio_path = None
        if audio and len(audio) == 1 and audio[0].filename:
            file = audio[0]
            a_suffix = Path(file.filename).suffix or ".mp3"
            audio_path = os.path.join(tmp_dir, f"audio-{uuid.uuid4().hex[:6]}{a_suffix}")
            with open(audio_path, "wb") as buf:
                shutil.copyfileobj(file.file, buf)
            tmp_files.append(audio_path)

            if overlay_params["showNowPlaying"]:
                if jobId:
                    progress_map[jobId] = {"progress": 0, "status": "Analyzing audio track..."}
                dur = await probe_audio_duration(audio_path)
                now_playing_segments.append({
                    "title": Path(file.filename).stem if file.filename else "Track 1",
                    "start": 0.0,
                    "end": dur
                })
        elif audio and len(audio) > 1:
            if jobId:
                progress_map[jobId] = {"progress": 0, "status": "Analyzing and merging audio tracks..."}
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

                if overlay_params["showNowPlaying"]:
                    dur = await probe_audio_duration(p)
                    now_playing_segments.append({
                        "title": Path(f.filename).stem if f.filename else f"Track {i+1}",
                        "start": current_time,
                        "end": current_time + dur
                    })
                    current_time += dur

            filter_complex += f"{concat_inputs}concat=n={len(audio)}:v=0:a=1[aout]"
            audio_args.extend([
                "-filter_complex", filter_complex,
                "-map", "[aout]",
                "-c:a", "aac", "-b:a", "192k",
                "-y", merged_audio
            ])
            await run_ffmpeg(audio_args)
            audio_path = merged_audio

        # Save videos
        video_paths = []
        for v in video:
            v_suffix = Path(v.filename).suffix or ".mp4"
            v_path = os.path.join(tmp_dir, f"vid-{uuid.uuid4().hex[:6]}{v_suffix}")
            with open(v_path, "wb") as buf:
                shutil.copyfileobj(v.file, buf)
            tmp_files.append(v_path)
            video_paths.append(v_path)

        if jobId:
            progress_map[jobId] = {"progress": 2, "status": "Analyzing durations..."}

        speed = float(videoSpeed)
        t_dur = float(transitionDuration)
        audio_dur = await probe_audio_duration(audio_path) if audio_path else 0.0

        base_durations = []
        base_sequence_dur = 0.0
        for vp in video_paths:
            orig_d = await get_video_duration(vp)
            adj_d = orig_d / speed if speed > 0 else orig_d
            base_durations.append(adj_d)
            base_sequence_dur += adj_d

        total_expected_duration = sum(base_durations)

        all_transitions = [
            "fade", "fadeblack", "fadewhite", "wipeleft", "wiperight",
            "circlecrop", "rectcrop", "distance", "radial", "pixelize", "hblur"
        ]
        parsed_transitions = all_transitions
        if transitionTypes:
            try:
                parsed = json.loads(transitionTypes)
                if isinstance(parsed, list) and parsed:
                    parsed_transitions = parsed
            except Exception:
                parts = [t.strip() for t in transitionTypes.split(",") if t.strip()]
                if parts:
                    parsed_transitions = parts

        is_none_trans = (t_dur <= 0 or (len(parsed_transitions) == 1 and parsed_transitions[0] == "none"))

        if len(video_paths) > 1 and not is_none_trans:
            total_expected_duration -= (len(video_paths) - 1) * t_dur
            base_sequence_dur = total_expected_duration

        target_length = targetDuration if targetDuration > 0 else audio_dur
        pts_multiplier = 1 / speed if speed > 0 else 1.0
        keep_audio = (keepOriginalAudio == "true")

        # ─── Single Video ───
        if len(video_paths) == 1:
            if jobId:
                progress_map[jobId] = {"progress": 5, "status": "Building filter graph..."}

            ffmpeg_args = []
            if audio_path or target_length > 0:
                ffmpeg_args.extend(["-stream_loop", "-1", "-fflags", "+genpts"])
            ffmpeg_args.extend(["-i", video_paths[0]])

            if audio_path:
                if target_length > 0:
                    ffmpeg_args.extend(["-stream_loop", "-1"])
                ffmpeg_args.extend(["-vn", "-i", audio_path])

            input_count = 1 + (1 if audio_path else 0)
            filter_complex = ""

            eff_dur = target_length or total_expected_duration or 600
            if has_any_overlay:
                filter_complex += f"[0:v]scale={resolution}:force_original_aspect_ratio=increase,crop={resolution},setsar=1,fps=30,setpts={pts_multiplier}*PTS,format=yuv420p[vbase]; "
                overlay = build_overlay_filters(overlay_params, eff_dur, input_count)
                filter_complex += overlay["filters"] + " "
                for arg in overlay["extra_inputs"]:
                    ffmpeg_args.append(arg)
            else:
                filter_complex += f"[0:v]scale={resolution}:force_original_aspect_ratio=increase,crop={resolution},setsar=1,fps=30,setpts={pts_multiplier}*PTS,format=yuv420p[v0]; [v0]null[vout]; "

            audio_node = ""
            if keep_audio and audio_path:
                filter_complex += "[0:a][1:a]amix=inputs=2:duration=longest[aout]"
                audio_node = "aout"
            elif keep_audio and not audio_path:
                audio_node = "0:a"
            elif not keep_audio and audio_path:
                audio_node = "1:a:0"

            fade_out_dur = 1.5
            fade_out_st = max(0, (target_length or total_expected_duration or 10) - fade_out_dur)
            if audio_node:
                filter_complex += f"; [{audio_node}]afade=t=out:st={fade_out_st}:d={fade_out_dur}[aout_final]"

            f_script = os.path.join(tmp_dir, f"filter-{tmp_id}.txt")
            with open(f_script, "w", encoding="utf-8") as f:
                f.write(filter_complex.strip().rstrip(";"))
            tmp_files.append(f_script)

            ffmpeg_args.extend(["-filter_complex_script", f_script, "-map", "[vout]"])
            if audio_node:
                ffmpeg_args.extend(["-map", "[aout_final]"])

            ffmpeg_args.extend(["-c:v", "libx264", "-preset", "medium", "-crf", "23", "-pix_fmt", "yuv420p"])
            if audio_path or keep_audio:
                ffmpeg_args.extend(["-c:a", "aac", "-b:a", "192k"])

            if target_length > 0:
                ffmpeg_args.extend(["-t", str(target_length)])
            else:
                ffmpeg_args.append("-shortest")

            ffmpeg_args.extend(["-y", "-progress", "pipe:1", output_path])
            await run_ffmpeg(ffmpeg_args, job_id=jobId, expected_duration=target_length or total_expected_duration or 10, progress_offset=5, progress_scale=90)

        # ─── Multi Video (Two-Pass) ───
        else:
            base_sequence_path = os.path.join(tmp_dir, f"basesequence-{tmp_id}.mp4")
            tmp_files.append(base_sequence_path)

            if jobId:
                progress_map[jobId] = {"progress": 5, "status": "Rendering base transitions (Pass 1)..."}

            pass1_args = []
            for vp in video_paths:
                pass1_args.extend(["-i", vp])

            filter_complex = ""
            for i in range(len(video_paths)):
                filter_complex += f"[{i}:v]scale={resolution}:force_original_aspect_ratio=increase,crop={resolution},setsar=1,fps=30,setpts={pts_multiplier}*PTS,format=yuv420p[v{i}]; "

            if is_none_trans:
                concat_nodes = "".join(f"[v{i}]" for i in range(len(video_paths)))
                filter_complex += f"{concat_nodes}concat=n={len(video_paths)}:v=1:a=0[vout]"
            else:
                last_node = "[v0]"
                cur_offset = base_durations[0] - t_dur

                fallback_map = {
                    "smoothleft": "slideleft", "smoothright": "slideright",
                    "glitch": "pixelize", "smoothpie": "circlecrop",
                    "zoomin": "fade", "hlslice": "fade", "dreamy": "hblur"
                }

                for i in range(1, len(video_paths)):
                    out_node = "[vout]" if i == len(video_paths) - 1 else f"[xf{i}]"
                    eff = random.choice(parsed_transitions)
                    eff = fallback_map.get(eff, eff)
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
            await run_ffmpeg(pass1_args, job_id=jobId, expected_duration=base_sequence_dur, progress_offset=5, progress_scale=60)

            # Pass 2: Overlays and audio loop
            if jobId:
                progress_map[jobId] = {"progress": 65, "status": "Adding overlays & audio (Pass 2)..."}

            loop_count = max(0, int(target_length // base_sequence_dur))
            pass2_args = ["-stream_loop", str(loop_count), "-i", base_sequence_path]

            if audio_path:
                if target_length > 0:
                    pass2_args.extend(["-stream_loop", "-1"])
                pass2_args.extend(["-vn", "-i", audio_path])

            p2_input_count = 1 + (1 if audio_path else 0)
            fade_out_dur = 1.5
            fade_out_st = max(0, (target_length or base_sequence_dur or 10) - fade_out_dur)

            if has_any_overlay:
                eff_dur = target_length or base_sequence_dur or 600
                overlay = build_overlay_filters(overlay_params, eff_dur, p2_input_count)
                for arg in overlay["extra_inputs"]:
                    pass2_args.append(arg)

                p2_filter = f"[0:v]null[vbase]; {overlay['filters']}"
                if audio_path:
                    p2_filter += f" [1:a]afade=t=out:st={fade_out_st}:d={fade_out_dur}[aout]"

                p2_script = os.path.join(tmp_dir, f"filter2-{tmp_id}.txt")
                with open(p2_script, "w", encoding="utf-8") as f:
                    f.write(p2_filter.strip().rstrip(";"))
                tmp_files.append(p2_script)

                pass2_args.extend(["-filter_complex_script", p2_script])
                if audio_path:
                    pass2_args.extend(["-map", "[vout]", "-map", "[aout]"])
                else:
                    pass2_args.extend(["-map", "[vout]"])
                pass2_args.extend(["-c:v", "libx264", "-preset", "medium", "-crf", "23", "-pix_fmt", "yuv420p"])
            else:
                if audio_path:
                    pass2_args.extend([
                        "-filter_complex", f"[1:a]afade=t=out:st={fade_out_st}:d={fade_out_dur}[aout]",
                        "-map", "0:v", "-map", "[aout]"
                    ])
                else:
                    pass2_args.extend(["-map", "0:v"])
                pass2_args.extend(["-c:v", "copy"])

            if audio_path:
                pass2_args.extend(["-c:a", "aac", "-b:a", "192k"])

            if target_length > 0:
                pass2_args.extend(["-t", str(target_length)])
            else:
                pass2_args.append("-shortest")

            pass2_args.extend(["-y", "-progress", "pipe:1", output_path])
            await run_ffmpeg(pass2_args, job_id=jobId, expected_duration=target_length or base_sequence_dur, progress_offset=65, progress_scale=30)

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
        print(f"Video mix failed: {e}")
        for f in tmp_files:
            try:
                if os.path.exists(f):
                    os.remove(f)
            except Exception:
                pass
        if jobId and jobId in progress_map:
            progress_map.pop(jobId, None)
        raise HTTPException(status_code=500, detail=f"Video mix failed: {str(e)}")
