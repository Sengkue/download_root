import os
import json
import uuid
import tempfile
from app.core.ffmpeg import escape_drawtext

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

def get_main_font() -> str:
    for f in ["C:/Windows/Fonts/LeelawUI.ttf", "C:/Windows/Fonts/arial.ttf", "C:/Windows/Fonts/consola.ttf"]:
        if os.path.exists(f):
            return f.replace("\\", "/").replace(":", "\\:")
    return ""

def get_symbol_font() -> str:
    for f in ["C:/Windows/Fonts/seguisym.ttf", "C:/Windows/Fonts/arial.ttf"]:
        if os.path.exists(f):
            return f.replace("\\", "/").replace(":", "\\:")
    return ""

def write_text_file(text: str, tmp_dir: str = None, tmp_files: list = None, prefix: str = "text") -> str:
    tmp_d = tmp_dir or tempfile.gettempdir()
    filepath = os.path.join(tmp_d, f"{prefix}_{uuid.uuid4().hex[:8]}.txt")
    with open(filepath, "w", encoding="utf-8-sig") as f:
        f.write(text)
    if tmp_files is not None:
        tmp_files.append(filepath)
    return filepath.replace("\\", "/").replace(":", "\\:")

def build_overlay_filters(params: dict, total_duration: float, extra_input_start_index: int, tmp_dir: str = None, tmp_files: list = None):
    # Parse resolution and compute scale factor relative to 1280x720 base
    resolution_str = str(params.get("resolution") or "1280:720")
    try:
        parts = resolution_str.replace("x", ":").split(":")
        res_w = int(parts[0])
        res_h = int(parts[1])
    except Exception:
        res_w, res_h = 1280, 720

    # Scale multiplier: 1920x1080 (FHD) is 1.5x of 1280x720 base
    if res_w >= res_h:
        scale = max(0.5, res_w / 1280.0)
    else:
        scale = max(0.5, res_w / 720.0)

    timer_enabled = params.get("timerEnabled", False)
    timer_mode = params.get("timerMode", "pomodoro")
    timer_minutes = float(params.get("timerMinutes") or 25)
    timer_break_minutes = float(params.get("timerBreakMinutes") or 5)
    timer_position = params.get("timerPosition", "top-right")
    timer_show_progress = params.get("timerShowProgress", False)
    timer_with_break = params.get("timerWithBreak", False)
    timer_pos_x = params.get("timerPosX")
    timer_pos_y = params.get("timerPosY")
    timer_font_size = int(round(float(params.get("timerFontSize") or 48) * scale))
    timer_box_border = max(8, int(round(14 * scale)))

    logo_enabled = params.get("logoEnabled", False)
    logo_path = params.get("logoPath")
    logo_position = params.get("logoPosition", "bottom-right")
    logo_opacity = float(params.get("logoOpacity") or 0.7)
    logo_size = int(round(float(params.get("logoSize") or 120) * scale))

    quotes_enabled = params.get("quotesEnabled", False)
    quotes_interval = float(params.get("quotesInterval") or 10) * 60
    quotes_duration = float(params.get("quotesDuration") or 15)
    quotes_position = params.get("quotesPosition", "bottom")
    quotes_font_size = int(round(32 * scale))
    quotes_box_border = max(6, int(round(12 * scale)))
    custom_quotes = params.get("customQuotes")

    show_now_playing = params.get("showNowPlaying", False)
    now_playing_segments = params.get("nowPlayingSegments") or []
    playlist_pos_x = params.get("playlistPosX")
    playlist_pos_y = params.get("playlistPosY")
    playlist_font_size = int(round(float(params.get("playlistFontSize") or 32) * scale))
    playlist_items_per_col = int(float(params.get("playlistItemsPerCol") or 15))
    playlist_col_gap = int(round(float(params.get("playlistColGap") or 380) * scale))

    main_font = get_main_font()
    sym_font = get_symbol_font()
    font_arg = f":fontfile='{main_font}'" if main_font else ""
    sym_font_arg = f":fontfile='{sym_font}'" if sym_font else ""

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

    # 1. Logo Watermark
    if logo_enabled and logo_path:
        is_last = (enabled_overlays[-1] == "logo")
        out_node = get_next_node(is_last)
        extra_inputs.extend(["-i", logo_path])
        logo_input_idx = input_idx
        input_idx += 1

        logo_margin = int(round(20 * scale))
        if logo_position == "top-left":
            ox, oy = f"{logo_margin}", f"{logo_margin}"
        elif logo_position == "top-right":
            ox, oy = f"W-w-{logo_margin}", f"{logo_margin}"
        elif logo_position == "bottom-left":
            ox, oy = f"{logo_margin}", f"H-h-{logo_margin}"
        else:
            ox, oy = f"W-w-{logo_margin}", f"H-h-{logo_margin}"

        filters += f"[{logo_input_idx}:v]scale={logo_size}:-1,format=rgba,colorchannelmixer=aa={logo_opacity}[logo_scaled]; "
        filters += f"[{current_node}][logo_scaled]overlay={ox}:{oy}[{out_node}]; "
        current_node = out_node

    # 2. Pomodoro / Song Timer
    if timer_enabled:
        is_last = (enabled_overlays[-1] == "timer")

        # Position coordinates with right-side safety clamping
        if timer_pos_x is not None and timer_pos_y is not None:
            # tx and ty are given as percentage of canvas
            # Ensure text + box border does not clip off the right or bottom edges
            tx = f"min(W-tw-(W*0.02)-{timer_box_border}\\, (W*{timer_pos_x}/100))"
            ty = f"min(H-th-(H*0.02)-{timer_box_border}\\, (H*{timer_pos_y}/100))"
        else:
            margin_x = int(round(30 * scale))
            margin_y = int(round(30 * scale))
            if timer_position == "top-left":
                tx, ty = f"{margin_x}", f"{margin_y}"
            elif timer_position == "top-right":
                tx, ty = f"w-tw-{margin_x}", f"{margin_y}"
            elif timer_position == "top-center":
                tx, ty = "(w-tw)/2", f"{margin_y}"
            elif timer_position == "bottom-left":
                tx, ty = f"{margin_x}", f"h-th-{int(round(60 * scale))}"
            elif timer_position == "bottom-right":
                tx, ty = f"w-tw-{margin_x}", f"h-th-{int(round(60 * scale))}"
            else:
                tx, ty = f"w-tw-{margin_x}", f"{margin_y}"

        if timer_mode == "persong" and now_playing_segments:
            for i, seg in enumerate(now_playing_segments):
                seg_is_last = is_last and (i == len(now_playing_segments) - 1)
                t_node = get_next_node(seg_is_last)
                st = seg.get("start", 0)
                et = seg.get("end", 0)
                timer_text = f"%{{eif\\: floor(({et}-t)/60) \\:d\\:2}}\\:%{{eif\\: mod(floor(({et}-t))\\,60) \\:d\\:2}}"
                filters += (
                    f"[{current_node}]drawtext=text='{timer_text}':"
                    f"fontsize={timer_font_size}:fontcolor=white:"
                    f"x={tx}:y={ty}:"
                    f"box=1:boxcolor=black@0.55:boxborderw={timer_box_border}:"
                    f"enable='between(t\\,{st}\\,{et})'{font_arg}[{t_node}]; "
                )
                current_node = t_node
        else:
            cycle_sec = timer_minutes * 60
            break_sec = (timer_break_minutes * 60) if timer_with_break else 0
            total_cycle_sec = cycle_sec + break_sec

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
                f"fontsize={timer_font_size}:fontcolor=white:"
                f"x={tx}:y={ty}:"
                f"box=1:boxcolor=black@0.55:boxborderw={timer_box_border}{font_arg}[{timer_node1}]; "
            )
            current_node = timer_node1

            if break_sec > 0:
                break_node = get_next_node(False)
                break_font = max(18, int(round(28 * scale)))
                break_y = f"{ty}+{int(round(60 * scale))}"
                break_border = max(4, int(round(8 * scale)))
                filters += (
                    f"[{current_node}]drawtext=text='BREAK':"
                    f"fontsize={break_font}:fontcolor=0x7CFC00:"
                    f"x={tx}:y={break_y}:"
                    f"box=1:boxcolor=black@0.5:boxborderw={break_border}:"
                    f"enable='gte(mod(t\\,{total_cycle_sec})\\,{cycle_sec})'{font_arg}[{break_node}]; "
                )
                current_node = break_node

            if timer_show_progress:
                bg_node = get_next_node(False)
                bar_h = max(4, int(round(8 * scale)))
                bar_y = f"ih-{int(round(12 * scale))}" if str(timer_position).startswith("bottom") else f"{int(round(105 * scale))}"
                filters += f"[{current_node}]drawbox=x=0:y={bar_y}:w=iw:h={bar_h}:color=black@0.4:t=fill[{bg_node}]; "
                current_node = bg_node

                if break_sec > 0:
                    work_node = get_next_node(False)
                    filters += (
                        f"[{current_node}]drawbox=x=0:y={bar_y}:w='mod(t\\,{total_cycle_sec})/{cycle_sec}*iw':"
                        f"h={bar_h}:color=0x845EC2@0.9:t=fill:enable='lt(mod(t\\,{total_cycle_sec})\\,{cycle_sec})'[{work_node}]; "
                    )
                    current_node = work_node

                    break_bar_node = get_next_node(is_last)
                    filters += (
                        f"[{current_node}]drawbox=x=0:y={bar_y}:w='(mod(t\\,{total_cycle_sec})-{cycle_sec})/{break_sec}*iw':"
                        f"h={bar_h}:color=0x7CFC00@0.9:t=fill:enable='gte(mod(t\\,{total_cycle_sec})\\,{cycle_sec})'[{break_bar_node}]; "
                    )
                    current_node = break_bar_node
                else:
                    progress_node = get_next_node(is_last)
                    filters += (
                        f"[{current_node}]drawbox=x=0:y={bar_y}:w='mod(t\\,{cycle_sec})/{cycle_sec}*iw':"
                        f"h={bar_h}:color=0x845EC2@0.9:t=fill[{progress_node}]; "
                    )
                    current_node = progress_node
            elif is_last:
                final_node = get_next_node(True)
                filters += f"[{current_node}]null[{final_node}]; "
                current_node = final_node

    # 3. Dynamic Quotes (Rendered safely via UTF-8 textfiles)
    if quotes_enabled:
        fade_time = min(2.0, max(0.2, quotes_duration / 4.0))
        quotes = DEFAULT_QUOTES
        if custom_quotes:
            try:
                parsed = json.loads(custom_quotes) if isinstance(custom_quotes, str) else custom_quotes
                if isinstance(parsed, list) and parsed:
                    quotes = [str(q).strip() for q in parsed if str(q).strip()]
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
            q_file = write_text_file(quote, tmp_dir=tmp_dir, tmp_files=tmp_files, prefix="quote")

            is_last = (enabled_overlays[-1] == "quotes" and i == num_quotes - 1)
            out_node = get_next_node(is_last)

            alpha_expr = f"if(lt(t\\,{start_time + fade_time})\\,(t-{start_time})/{fade_time}\\,if(gt(t\\,{end_time - fade_time})\\,({end_time}-t)/{fade_time}\\,1))"
            filters += (
                f"[{current_node}]drawtext=textfile='{q_file}':"
                f"fontsize={quotes_font_size}:fontcolor=white:alpha='{alpha_expr}':"
                f"x=(w-tw)/2:y={quote_y}:"
                f"box=1:boxcolor=black@0.45:boxborderw={quotes_box_border}:"
                f"enable='between(t\\,{start_time}\\,{end_time})'{font_arg}[{out_node}]; "
            )
            current_node = out_node

        if num_quotes == 0 and enabled_overlays[-1] == "quotes":
            final_node = get_next_node(True)
            filters += f"[{current_node}]null[{final_node}]; "
            current_node = final_node

    # 4. Now Playing / Playlist (Full interactive list with ▶ indicator)
    if show_now_playing and now_playing_segments:
        start_x = f"(W*{playlist_pos_x or 5}/100)"
        start_y = f"(H*{playlist_pos_y or 7}/100)"
        p_size = playlist_font_size
        line_height = p_size + max(4, int(round(8 * scale)))
        box_border = max(4, int(round(8 * scale)))
        items_per_col = playlist_items_per_col
        col_gap = playlist_col_gap

        # Draw inactive playlist items
        for i, seg in enumerate(now_playing_segments):
            title = f"{i + 1}. {seg.get('title', 'Track')}"
            t_file = write_text_file(title, tmp_dir=tmp_dir, tmp_files=tmp_files, prefix="title_inact")
            out_node = get_next_node(False)

            row_idx = i % items_per_col
            col_idx = i // items_per_col
            x_pos = f"({start_x} + ({col_idx} * {col_gap}))"
            y_pos = f"({start_y} + ({row_idx} * {line_height}))"
            text_offset = max(int(round(20 * scale)), int(p_size * 0.9))

            filters += (
                f"[{current_node}]drawtext=textfile='{t_file}':"
                f"fontsize={p_size}:fontcolor=white:borderw={max(1, int(round(2 * scale)))}:bordercolor=black@0.6:"
                f"x=({x_pos} + {text_offset}):y={y_pos}{font_arg}[{out_node}]; "
            )
            current_node = out_node

        # Draw active highlighted items with ▶ icon
        for i, seg in enumerate(now_playing_segments):
            title = f"{i + 1}. {seg.get('title', 'Track')}"
            t_file = write_text_file(title, tmp_dir=tmp_dir, tmp_files=tmp_files, prefix="title_act")
            is_last = (enabled_overlays[-1] == "nowplaying" and i == len(now_playing_segments) - 1)

            row_idx = i % items_per_col
            col_idx = i // items_per_col
            st = seg.get("start", 0)
            et = seg.get("end", 0)
            x_pos = f"({start_x} + ({col_idx} * {col_gap}))"
            y_pos = f"({start_y} + ({row_idx} * {line_height}))"
            text_offset = max(int(round(20 * scale)), int(p_size * 0.9))

            # Play icon ▶
            icon_node = get_next_node(False)
            filters += (
                f"[{current_node}]drawtext=text='▶':"
                f"fontsize={p_size}:fontcolor=white:"
                f"x={x_pos}:y={y_pos}:"
                f"enable='between(t\\,{st}\\,{et})'{sym_font_arg}[{icon_node}]; "
            )
            current_node = icon_node

            # Highlighted title
            out_node = get_next_node(is_last)
            filters += (
                f"[{current_node}]drawtext=textfile='{t_file}':"
                f"fontsize={p_size}:fontcolor=white:"
                f"x=({x_pos} + {text_offset}):y={y_pos}:"
                f"box=1:boxcolor=0x845EC2@0.7:boxborderw={box_border}:"
                f"enable='between(t\\,{st}\\,{et})'{font_arg}[{out_node}]; "
            )
            current_node = out_node

    return {
        "filters": filters,
        "extra_inputs": extra_inputs,
        "input_index_offset": input_idx - extra_input_start_index
    }
