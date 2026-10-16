import json
from config.ffmpeg_utils import escape_drawtext

DEFAULT_QUOTES = [
    "Stay focused. You are doing great!",
    "Deep Work Session in Progress...",
    "One task at a time. You got this!",
    "Discipline equals freedom.",
    "Small steps lead to big results.",
    "Focus on progress, not perfection.",
    "Your future self will thank you.",
    "Eliminate distractions. Stay sharp.",
    "Every minute counts. Keep going!",
    "The secret of getting ahead is getting started.",
    "Breathe. Focus. Execute.",
    "Hard work beats talent when talent doesn't work hard.",
    "Almost there! Keep pushing!",
    "Success is built one session at a time.",
    "You are stronger than your excuses.",
    "This is your time to shine.",
    "Embrace the grind.",
    "Break coming soon. Stay strong!",
    "Turn your can'ts into cans.",
    "Consistency is the key to mastery."
]

def build_overlay_filters(params: dict, total_duration: float, extra_input_start_index: int):
    timer_enabled = params.get("timerEnabled", False)
    timer_minutes = int(params.get("timerMinutes") or 25)
    timer_break_minutes = int(params.get("timerBreakMinutes") or 5)
    timer_position = params.get("timerPosition", "top-right")
    timer_show_progress = params.get("timerShowProgress", False)
    timer_with_break = params.get("timerWithBreak", False)

    logo_enabled = params.get("logoEnabled", False)
    logo_path = params.get("logoPath")
    logo_position = params.get("logoPosition", "bottom-right")
    logo_opacity = float(params.get("logoOpacity") or 0.7)
    logo_size = int(params.get("logoSize") or 120)

    quotes_enabled = params.get("quotesEnabled", False)
    quotes_interval = int(params.get("quotesInterval") or 10) * 60
    quotes_duration = int(params.get("quotesDuration") or 15)
    quotes_position = params.get("quotesPosition", "bottom")
    custom_quotes = params.get("customQuotes")

    show_now_playing = params.get("showNowPlaying", False)
    now_playing_segments = params.get("nowPlayingSegments") or []

    filters = ""
    current_node = "vbase"
    next_node_id = 0
    extra_inputs = []
    input_idx = extra_input_start_index

    enabled_overlays = []
    if timer_enabled:
        enabled_overlays.append("timer")
    if logo_enabled and logo_path:
        enabled_overlays.append("logo")
    if quotes_enabled:
        enabled_overlays.append("quotes")
    if show_now_playing and now_playing_segments:
        enabled_overlays.append("nowplaying")

    def get_next_node(is_final: bool):
        nonlocal next_node_id
        if is_final:
            return "vout"
        val = f"ovl{next_node_id}"
        next_node_id += 1
        return val

    if not enabled_overlays:
        return {
            "filters": f"[{current_node}]null[vout]",
            "extra_inputs": [],
            "input_index_offset": 0
        }

    # 1. Logo watermark
    if logo_enabled and logo_path:
        is_last = (enabled_overlays[-1] == "logo")
        out_node = get_next_node(is_last)
        extra_inputs.extend(["-i", logo_path])
        logo_input_idx = input_idx
        input_idx += 1

        if logo_position == "top-left":
            ox, oy = "20", "20"
        elif logo_position == "top-right":
            ox, oy = "W-w-20", "20"
        elif logo_position == "bottom-left":
            ox, oy = "20", "H-h-20"
        else:
            ox, oy = "W-w-20", "H-h-20"

        filters += f"[{logo_input_idx}:v]scale={logo_size}:-1,format=rgba,colorchannelmixer=aa={logo_opacity}[logo_scaled]; "
        filters += f"[{current_node}][logo_scaled]overlay={ox}:{oy}[{out_node}]; "
        current_node = out_node

    # 2. Pomodoro Timer
    if timer_enabled:
        is_last = (enabled_overlays[-1] == "timer")
        cycle_sec = timer_minutes * 60
        break_sec = (timer_break_minutes * 60) if timer_with_break else 0
        total_cycle_sec = cycle_sec + break_sec

        if timer_position == "top-left":
            tx, ty = "30", "30"
        elif timer_position == "top-right":
            tx, ty = "w-tw-30", "30"
        elif timer_position == "top-center":
            tx, ty = "(w-tw)/2", "30"
        elif timer_position == "bottom-left":
            tx, ty = "30", "h-th-60"
        elif timer_position == "bottom-right":
            tx, ty = "w-tw-30", "h-th-60"
        else:
            tx, ty = "w-tw-30", "30"

        if break_sec > 0:
            timer_text = (
                f"%{{eif\\: if(lt(mod(t\\,{total_cycle_sec})\\,{cycle_sec})\\, "
                f"floor(({cycle_sec}-mod(t\\,{total_cycle_sec}))/60)\\, "
                f"floor(({total_cycle_sec}-mod(t\\,{total_cycle_sec}))/60) ) \\:d\\:2}}\\:"
                f"%{{eif\\: if(lt(mod(t\\,{total_cycle_sec})\\,{cycle_sec})\\, "
                f"mod(floor({cycle_sec}-mod(t\\,{total_cycle_sec}))\\,60)\\, "
                f"mod(floor({total_cycle_sec}-mod(t\\,{total_cycle_sec}))\\,60) ) \\:d\\:2}}"
            )
        else:
            timer_text = (
                f"%{{eif\\: floor(({cycle_sec}-mod(t\\,{cycle_sec}))/60) \\:d\\:2}}\\:"
                f"%{{eif\\: mod(floor({cycle_sec}-mod(t\\,{cycle_sec}))\\,60) \\:d\\:2}}"
            )

        timer_node1 = get_next_node(False)
        filters += (
            f"[{current_node}]drawtext=text='{timer_text}':"
            f"fontsize=48:fontcolor=white:"
            f"x={tx}:y={ty}:"
            f"box=1:boxcolor=black@0.55:boxborderw=14:"
            f"fontfile='C\\:/Windows/Fonts/consola.ttf'[{timer_node1}]; "
        )
        current_node = timer_node1

        if break_sec > 0:
            break_node = get_next_node(False)
            filters += (
                f"[{current_node}]drawtext=text='BREAK':"
                f"fontsize=28:fontcolor=0x7CFC00:"
                f"x={tx}:y={ty}+60:"
                f"box=1:boxcolor=black@0.5:boxborderw=8:"
                f"fontfile='C\\:/Windows/Fonts/consola.ttf':"
                f"enable='gte(mod(t\\,{total_cycle_sec})\\,{cycle_sec})'[{break_node}]; "
            )
            current_node = break_node

        if timer_show_progress:
            bg_node = get_next_node(False)
            bar_y = "ih-12" if str(timer_position).startswith("bottom") else "105"
            filters += f"[{current_node}]drawbox=x=0:y={bar_y}:w=iw:h=8:color=black@0.4:t=fill[{bg_node}]; "
            current_node = bg_node

            if break_sec > 0:
                work_node = get_next_node(False)
                filters += (
                    f"[{current_node}]drawbox=x=0:y={bar_y}:w='mod(t\\,{total_cycle_sec})/{cycle_sec}*iw':"
                    f"h=8:color=0x845EC2@0.9:t=fill:enable='lt(mod(t\\,{total_cycle_sec})\\,{cycle_sec})'[{work_node}]; "
                )
                current_node = work_node

                break_bar_node = get_next_node(is_last)
                filters += (
                    f"[{current_node}]drawbox=x=0:y={bar_y}:w='(mod(t\\,{total_cycle_sec})-{cycle_sec})/{break_sec}*iw':"
                    f"h=8:color=0x7CFC00@0.9:t=fill:enable='gte(mod(t\\,{total_cycle_sec})\\,{cycle_sec})'[{break_bar_node}]; "
                )
                current_node = break_bar_node
            else:
                progress_node = get_next_node(is_last)
                filters += (
                    f"[{current_node}]drawbox=x=0:y={bar_y}:w='mod(t\\,{cycle_sec})/{cycle_sec}*iw':"
                    f"h=8:color=0x845EC2@0.9:t=fill[{progress_node}]; "
                )
                current_node = progress_node
        elif is_last:
            final_node = get_next_node(True)
            filters += f"[{current_node}]null[{final_node}]; "
            current_node = final_node

    # 3. Dynamic Quotes
    if quotes_enabled:
        fade_time = 2
        quotes = DEFAULT_QUOTES
        if custom_quotes:
            try:
                parsed = json.loads(custom_quotes) if isinstance(custom_quotes, str) else custom_quotes
                if isinstance(parsed, list) and parsed:
                    quotes = [q for q in parsed if str(q).strip()]
            except Exception:
                lines = [l.strip() for l in str(custom_quotes).split("\n") if l.strip()]
                if lines:
                    quotes = lines

        if quotes_position == "top":
            quote_y = "h*0.15"
        elif quotes_position == "center":
            quote_y = "(h-th)/2"
        else:
            quote_y = "h*0.82"

        max_quotes = int(total_duration // quotes_interval) if quotes_interval > 0 else 0
        num_quotes = min(max_quotes, 60)

        for i in range(num_quotes):
            start_time = (i + 1) * quotes_interval - quotes_duration
            end_time = start_time + quotes_duration
            if start_time < 0:
                continue

            quote = quotes[i % len(quotes)]
            escaped_quote = escape_drawtext(quote)
            is_last = (enabled_overlays[-1] == "quotes" and i == num_quotes - 1)
            out_node = get_next_node(is_last)

            alpha_expr = f"if(lt(t\\,{start_time + fade_time})\\,(t-{start_time})/{fade_time}\\,if(gt(t\\,{end_time - fade_time})\\,({end_time}-t)/{fade_time}\\,1))"
            filters += (
                f"[{current_node}]drawtext=text='{escaped_quote}':"
                f"fontsize=32:fontcolor=white:alpha='{alpha_expr}':"
                f"x=(w-tw)/2:y={quote_y}:"
                f"box=1:boxcolor=black@0.45:boxborderw=12:"
                f"fontfile='C\\:/Windows/Fonts/consola.ttf':"
                f"enable='between(t\\,{start_time}\\,{end_time})'[{out_node}]; "
            )
            current_node = out_node

        if num_quotes == 0 and enabled_overlays[-1] == "quotes":
            final_node = get_next_node(True)
            filters += f"[{current_node}]null[{final_node}]; "
            current_node = final_node

    # 4. Now Playing
    if show_now_playing and now_playing_segments:
        fade_time = 1.0
        for i, seg in enumerate(now_playing_segments):
            title = f"🎵 {seg.get('title', 'Unknown')}"
            escaped_title = escape_drawtext(title)
            is_last = (enabled_overlays[-1] == "nowplaying" and i == len(now_playing_segments) - 1)
            out_node = get_next_node(is_last)

            start_time = seg.get("start", 0)
            end_time = seg.get("end", 0)
            alpha_expr = f"if(lt(t\\,{start_time + fade_time})\\,(t-{start_time})/{fade_time}\\,if(gt(t\\,{end_time - fade_time})\\,({end_time}-t)/{fade_time}\\,1))"

            filters += (
                f"[{current_node}]drawtext=text='{escaped_title}':"
                f"fontsize=36:fontcolor=white:alpha='{alpha_expr}':"
                f"x=40:y=H-h-40:"
                f"box=1:boxcolor=black@0.6:boxborderw=10:"
                f"fontfile='C\\:/Windows/Fonts/consola.ttf':"
                f"enable='between(t\\,{start_time}\\,{end_time})'[{out_node}]; "
            )
            current_node = out_node

    return {
        "filters": filters,
        "extra_inputs": extra_inputs,
        "input_index_offset": input_idx - extra_input_start_index
    }
