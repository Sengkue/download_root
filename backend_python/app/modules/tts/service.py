import os
import re
import json
import base64
import hashlib
import asyncio
from pathlib import Path
from typing import Optional, List, Dict, Any, Tuple
from dotenv import load_dotenv
import httpx

from app.core.config import UPLOAD_DIR

load_dotenv()

TTS_CACHE_DIR = UPLOAD_DIR / "tts_cache"
TTS_CACHE_DIR.mkdir(parents=True, exist_ok=True)

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "")

# Initialize ElevenLabs Client
eleven_client = None
if ELEVENLABS_API_KEY:
    try:
        from elevenlabs.client import ElevenLabs
        # Use verify=False to prevent Windows SSL interception failures
        custom_http = httpx.Client(verify=False, timeout=60.0)
        eleven_client = ElevenLabs(api_key=ELEVENLABS_API_KEY, httpx_client=custom_http)
        print("[TTS] ElevenLabs client initialized successfully with API Key")
    except Exception as e:
        print(f"[TTS] Failed to initialize ElevenLabs client: {e}")

# Edge-TTS Fallback
try:
    import edge_tts
    HAS_EDGE_TTS = True
except ImportError:
    HAS_EDGE_TTS = False

# Popular Default ElevenLabs Voices
DEFAULT_ELEVEN_VOICES = {
    "storyteller_male": "JBFqnCBsd6RMkjVDRZzb",   # George - Warm, Captivating Storyteller
    "storyteller_female": "EXAVITQu4vr4xnSDxMaL", # Sarah - Mature, Reassuring, Confident
    "casual_male": "IKne3meq5aSn9XLyUdCD",        # Charlie - Deep, Confident
    "enthusiast_female": "FGY2WhTYpPnrIDTdsKH5",  # Laura - Quirky, Enthusiast
    "resonant_male": "CwhRBWXzGAHq8TQ4Fs17"       # Roger - Laid-back, Resonant
}

# Edge-TTS Neural Fallback Voices
EDGE_VOICE_MAP = {
    "lo": {
        "female": "lo-LA-KeomanyNeural",
        "male": "lo-LA-ChanthavongNeural"
    },
    "hmn": {
        "female": "th-TH-PremwadeeNeural",
        "male": "th-TH-NiwatNeural"
    },
    "th": {
        "female": "th-TH-PremwadeeNeural",
        "male": "th-TH-NiwatNeural"
    },
    "en": {
        "female": "en-US-JennyNeural",
        "male": "en-US-GuyNeural"
    }
}

# Lao Unicode to Thai script phonetic mapping
LAO_TO_THAI_MAP = {
    'ກ': 'ก', 'ຂ': 'ข', 'ຄ': 'ค', 'ງ': 'ง',
    'ຈ': 'จ', 'ສ': 'ส', 'ຊ': 'ซ', 'ຍ': 'ย',
    'ດ': 'ด', 'ຕ': 'ต', 'ຖ': 'ถ', 'ທ': 'ท',
    'ນ': 'น', 'ບ': 'บ', 'ປ': 'ป', 'ຜ': 'ผ',
    'ຝ': 'ฝ', 'ພ': 'พ', 'ຟ': 'ฟ', 'ມ': 'ม',
    'ຢ': 'ย', 'ຣ': 'ร', 'ລ': 'ล', 'ວ': 'ว',
    'ຫ': 'ห', 'ອ': 'อ', 'ຮ': 'ฮ',
    'ໜ': 'หน', 'ໝ': 'หม', 'ຫຼ': 'หล', 'ຫວ': 'หว',
    'ະ': 'ะ', 'າ': 'า', 'ິ': 'ิ', 'ີ': 'ี',
    'ຶ': 'ึ', 'ື': 'ื', 'ຸ': 'ุ', 'ູ': 'ู',
    'ົ': '', 'ຼ': 'ล', 'ຽ': 'ีย',
    'ເ': 'เ', 'ແ': 'แ', 'ໂ': 'โ', 'ໃ': 'ใ', 'ໄ': 'ไ',
    '່': '่', '້': '้', '໊': '๊', '໋': '๋', '໌': '์',
    'ໍ': 'อ', 'ັ': 'ั'
}

# Comprehensive Hmong RPA vocabulary dictionary
HMONG_WORD_DICT = {
    'nyob': 'ย็อบ', 'zoo': 'ซอง', 'sawv': 'ซาว', 'daws': 'ดาว',
    'nyobzoo': 'ย็อบซอง', 'ua': 'อัว', 'tsaug': 'เจา', 'uatsaug': 'อัวเจา',
    'thov': 'ทอ', 'txim': 'จีม', 'thovtxim': 'ทอจีม', 'sib': 'ซี',
    'ntsib': 'นจีบ', 'dua': 'ดัว', 'sibntsibdua': 'ซีนจีบดัว',
    'los': 'ลอ', 'mus': 'มู', 'kuv': 'กู', 'koj': 'ก้อ',
    'nws': 'นือ', 'peb': 'เป', 'neb': 'เน', 'lawv': 'ลาว',
    'luag': 'ลัว', 'sawvdaws': 'ซาวดาว', 'tus': 'ตู', 'cov': 'จอ',
    'ib': 'อี้', 'ob': 'ออ', 'leej': 'เลง', 'tib': 'ตี',
    'thaum': 'เถา', 'ub': 'อู่', 'thaumub': 'เถาอู่',
    'muaj': 'มั่ว', 'tug': 'ตู', 'tsov': 'โจว', 'loj': 'ล้อ',
    'heev': 'เฮง', 'hav': 'ฮาว', 'zoov': 'ซอง', 'havzoov': 'ฮาวซอง',
    'ntsuab': 'นจวบ', 'txhua': 'ชัว', 'hnub': 'นูบ', 'tsiaj': 'เจี่ย',
    'ntshai': 'ไฉ', 'ntawd': 'นเตา', 'vim': 'วิม', 'nyiam': 'เนียม',
    'ntes': 'นเต้', 'noj': 'น้อ', 'luav': 'ลัว', 'me': 'เม',
    'hais': 'ไฮ', 'tias': 'เตีย', 'tsis': 'จิ', 'txhob': 'ช็อบ',
    'tom': 'ตอม', 'lub': 'ลูบ', 'qhov': 'กอง', 'dej': 'เด',
    'qhovdej': 'กองเด', 'tob': 'ต็อบ', 'npau': 'เปา', 'taws': 'ตาว',
    'npautaws': 'เปาตาว', 'thiab': 'เทียบ', 'kom': 'กอม', 'coj': 'จ้อ',
    'saib': 'ไซ', 'ntsia': 'นเจีย', 'duab': 'ดวบ', 'tab': 'ตาบ',
    'sis': 'ซิ', 'tabsis': 'ตาบซิ', 'xav': 'ซาว', 'yog': 'ยอ',
    'lwm': 'ลืม', 'dhia': 'เดีย', 'thiaj': 'เทีย', 'dim': 'ดิม',
    'txoj': 'จอ', 'sia': 'เสี่ย', 'txojsia': 'จอเสี่ย', 'ntse': 'นเจ',
    'qaib': 'ไก่', 'hli': 'หลี', 'noog': 'น็อง', 'quav': 'กวา',
    'liab': 'เลียบ', 'ntoo': 'นตอง', 'txiv': 'จี', 'ncaj': 'นจา',
    'ncees': 'นเจง', 'kub': 'กูบ', 'nyiaj': 'เนีย', 'os': 'ออ',
    'nteg': 'นเตง', 'qe': 'เก', 'paj': 'ปา', 'ntaub': 'นเตา',
    'pajntaub': 'ปานเตา', 'lus': 'ลู', 'hmoob': 'หม็อบ', 'moob': 'ม็อบ',
    'kawm': 'กำ', 'ntawv': 'นเตา', 'nyuam': 'ญวม', 'txawj': 'จ้อ',
    'pab': 'ปาบ', 'lubneej': 'ลูบเนง', 'npe': 'มเป', 'hu': 'ฮู',
    'li': 'ลี', 'cas': 'จา', 'no': 'นอ', 'pom': 'ปอม',
    'hauv': 'เฮา', 'roob': 'รอง', 'ntuj': 'นตู', 'zos': 'ซอ',
    'tsev': 'เจ', 'caij': 'ไจ', 'nyoog': 'ญ็อง', 'sij': 'ซี',
    'hawm': 'ฮัม', 'sijhawm': 'ซีฮัม'
}

HMONG_INITIALS = [
    ('ntsh', 'นช'), ('ntxh', 'นช'), ('nplh', 'มผล'), ('plh', 'ผล'),
    ('tsh', 'ช'), ('txh', 'ช'), ('nch', 'นช'), ('nkh', 'งค'),
    ('nph', 'มพ'), ('nqh', 'งค'), ('nrh', 'นทร'), ('nth', 'นท'),
    ('npl', 'มปล'), ('ml', 'มล'), ('nc', 'นจ'), ('nk', 'งก'),
    ('np', 'มป'), ('nq', 'งก'), ('nr', 'นตร'), ('nt', 'นต'),
    ('ny', 'ญ'), ('pl', 'ปล'), ('rh', 'ทร'), ('th', 'ท'),
    ('ts', 'จ'), ('tx', 'จ'), ('xy', 'ซย'), ('ch', 'ช'),
    ('dh', 'ด'), ('hl', 'หล'), ('hm', 'หม'), ('hn', 'หน'),
    ('kh', 'ค'), ('ph', 'พ'), ('qh', 'ค'), ('c', 'จ'),
    ('d', 'ด'), ('f', 'ฟ'), ('h', 'ฮ'), ('k', 'ก'),
    ('l', 'ล'), ('m', 'ม'), ('n', 'น'), ('p', 'ป'),
    ('q', 'ก'), ('r', 'ตร'), ('s', 'ซ'), ('t', 'ต'),
    ('v', 'ว'), ('x', 'ซ'), ('y', 'ย'), ('z', 'จ')
]

HMONG_VOWELS = [
    ('ai', lambda c: f'ไ{c}'),
    ('au', lambda c: f'เ{c}า'),
    ('aw', lambda c: f'{c}าว'),
    ('ee', lambda c: f'เ{c}็ง'),
    ('ia', lambda c: f'เ{c}ีย'),
    ('oo', lambda c: f'{c}อง'),
    ('ua', lambda c: f'{c}ัว'),
    ('a',  lambda c: f'{c}า'),
    ('e',  lambda c: f'เ{c}'),
    ('i',  lambda c: f'{c}ี'),
    ('o',  lambda c: f'{c}อ'),
    ('u',  lambda c: f'{c}ู'),
    ('w',  lambda c: f'{c}ือ')
]

def lao_to_thai(text: str) -> str:
    return "".join(LAO_TO_THAI_MAP.get(c, c) for c in text)

def hmong_word_to_thai(word: str) -> str:
    w = word.strip().lower()
    if not w:
        return ""
    punct_prefix = re.match(r'^[^a-z]+', w)
    punct_suffix = re.search(r'[^a-z]+$', w)
    prefix_str = punct_prefix.group(0) if punct_prefix else ""
    suffix_str = punct_suffix.group(0) if punct_suffix else ""

    clean = re.sub(r'[^a-z]', '', w)
    if not clean:
        return word

    if clean in HMONG_WORD_DICT:
        return f"{prefix_str}{HMONG_WORD_DICT[clean]}{suffix_str}"

    tone_char = ""
    if len(clean) > 1 and clean[-1] in "bjvsgmd":
        tone_char = clean[-1]
        clean = clean[:-1]

    init_thai = 'อ'
    for ini, th in HMONG_INITIALS:
        if clean.startswith(ini):
            init_thai = th
            clean = clean[len(ini):]
            break

    vowel_res = f'{init_thai}า'
    for vow, func in HMONG_VOWELS:
        if clean.startswith(vow):
            vowel_res = func(init_thai)
            break

    if tone_char in ('j', 's', 'g', 'm'):
        vowel_res += '่'
    elif tone_char == 'b':
        vowel_res += '้'
    elif tone_char in ('v', 'd'):
        vowel_res += '๋'

    return f"{prefix_str}{vowel_res}{suffix_str}"

def hmong_to_phonetic(text: str) -> str:
    tokens = text.split()
    return " ".join([hmong_word_to_thai(tok) for tok in tokens])

def extract_word_timestamps(characters: List[str], start_times: List[float], end_times: List[float]) -> List[Dict[str, Any]]:
    """Converts character-level timestamps into word-level start & end timestamps."""
    words = []
    curr = []
    w_start = None
    prev_end = 0.0

    for c, s, e in zip(characters, start_times, end_times):
        if c in (' ', '\n', '\t'):
            if curr:
                words.append({
                    'word': ''.join(curr),
                    'start': round(w_start, 3) if w_start is not None else 0.0,
                    'end': round(prev_end, 3)
                })
                curr = []
                w_start = None
        else:
            if w_start is None:
                w_start = s
            curr.append(c)
        prev_end = e

    if curr:
        words.append({
            'word': ''.join(curr),
            'start': round(w_start, 3) if w_start is not None else 0.0,
            'end': round(prev_end, 3)
        })
    return words

def get_elevenlabs_user_info() -> Dict[str, Any]:
    """Check ElevenLabs account status and credit usage."""
    if not eleven_client:
        return {"configured": False, "error": "ElevenLabs API key not configured"}
    try:
        user = eleven_client.user.get()
        return {
            "configured": True,
            "tier": user.subscription.tier,
            "character_count": user.subscription.character_count,
            "character_limit": user.subscription.character_limit,
            "can_extend_character_limit": user.subscription.can_extend_character_limit
        }
    except Exception as e:
        return {"configured": False, "error": str(e)}

def list_elevenlabs_voices() -> List[Dict[str, Any]]:
    """Retrieve all available voices from ElevenLabs."""
    if not eleven_client:
        return []
    try:
        res = eleven_client.voices.get_all()
        voices = []
        for v in res.voices:
            voices.append({
                "voice_id": v.voice_id,
                "name": v.name,
                "category": v.category,
                "description": getattr(v, "description", "") or "",
                "preview_url": getattr(v, "preview_url", "") or ""
            })
        return voices
    except Exception as e:
        print(f"[TTS] Error fetching ElevenLabs voices: {e}")
        return []

async def _synthesize_edge_tts(text: str, voice_name: str) -> bytes:
    """Fallback Edge-TTS audio generator."""
    if not HAS_EDGE_TTS:
        return b""
    try:
        communicate = edge_tts.Communicate(text, voice_name)
        chunks = []
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                chunks.append(chunk["data"])
        return b"".join(chunks)
    except Exception as e:
        print(f"[TTS] Edge-TTS error: {e}")
        return b""

def synthesize_with_elevenlabs(
    text: str,
    voice_id: Optional[str] = None,
    model_id: str = "eleven_multilingual_v2"
) -> Tuple[bytes, List[Dict[str, Any]]]:
    """
    Synthesize audio using ElevenLabs API and compute exact word timestamps.
    """
    if not eleven_client:
        raise RuntimeError("ElevenLabs client not initialized")

    target_voice = voice_id or DEFAULT_ELEVEN_VOICES["storyteller_male"]

    # Generate speech with timestamps
    response = eleven_client.text_to_speech.convert_with_timestamps(
        text=text,
        voice_id=target_voice,
        model_id=model_id
    )

    audio_bytes = base64.b64decode(response.audio_base_64)
    alignment = getattr(response, "alignment", None)
    word_timestamps = []

    if alignment:
        chars = alignment.characters
        starts = alignment.character_start_times_seconds
        ends = alignment.character_end_times_seconds
        word_timestamps = extract_word_timestamps(chars, starts, ends)

    return audio_bytes, word_timestamps

async def generate_speech_audio_async(
    text: str,
    lang: str = "lo",
    gender: str = "male",
    voice_id: Optional[str] = None,
    engine: str = "elevenlabs"
) -> Tuple[bytes, List[Dict[str, Any]]]:
    """
    Master speech generator:
    1. Uses ElevenLabs when configured (with real word timestamps).
    2. Fallback to Edge Neural voice if ElevenLabs is unavailable or edge engine is selected.
    """
    clean_text = text.strip()
    if not clean_text:
        return b"", []

    normalized_lang = lang.lower().strip()
    norm_gender = "male" if "male" in gender.lower() and "female" not in gender.lower() else "female"

    # Cache Key
    cache_key = hashlib.md5(f"{engine}:{normalized_lang}:{norm_gender}:{voice_id}:{clean_text}".encode("utf-8")).hexdigest()
    cache_audio = TTS_CACHE_DIR / f"{cache_key}.mp3"
    cache_meta = TTS_CACHE_DIR / f"{cache_key}.json"

    if cache_audio.exists() and cache_meta.exists():
        try:
            meta = json.loads(cache_meta.read_text(encoding="utf-8"))
            return cache_audio.read_bytes(), meta.get("word_timestamps", [])
        except Exception:
            pass

    audio_bytes = b""
    word_timestamps = []

    # 1. Try ElevenLabs
    if engine == "elevenlabs" and eleven_client:
        try:
            chosen_voice = voice_id
            if not chosen_voice:
                chosen_voice = DEFAULT_ELEVEN_VOICES["storyteller_male"] if norm_gender == "male" else DEFAULT_ELEVEN_VOICES["storyteller_female"]

            # Run in thread pool to prevent blocking event loop
            loop = asyncio.get_event_loop()
            audio_bytes, word_timestamps = await loop.run_in_executor(
                None,
                synthesize_with_elevenlabs,
                clean_text,
                chosen_voice,
                "eleven_multilingual_v2"
            )
        except Exception as e:
            print(f"[TTS] ElevenLabs synthesis failed, using fallback: {e}")
            audio_bytes = b""

    # 2. Fallback to Edge-TTS Neural if ElevenLabs failed or edge chosen
    if not audio_bytes and HAS_EDGE_TTS:
        voice_edge = EDGE_VOICE_MAP.get(normalized_lang, EDGE_VOICE_MAP["lo"]).get(norm_gender, "lo-LA-KeomanyNeural")
        
        # Phonetic transcription for Hmong
        synth_text = clean_text
        if normalized_lang in ("hmn", "mww", "hnj", "hmong"):
            synth_text = hmong_to_phonetic(clean_text)

        audio_bytes = await _synthesize_edge_tts(synth_text, voice_edge)

        # Estimate word timestamps evenly for fallback
        if audio_bytes:
            words = clean_text.split()
            # Estimate duration ~0.35s per word
            est_dur = max(2.0, len(words) * 0.38)
            time_per_word = est_dur / max(1, len(words))
            for i, w in enumerate(words):
                word_timestamps.append({
                    "word": w,
                    "start": round(i * time_per_word, 3),
                    "end": round((i + 1) * time_per_word, 3)
                })

    # Save to Cache
    if audio_bytes:
        try:
            cache_audio.write_bytes(audio_bytes)
            cache_meta.write_text(json.dumps({"word_timestamps": word_timestamps}, ensure_ascii=False), encoding="utf-8")
        except Exception as e:
            print(f"[TTS] Cache write error: {e}")

    return audio_bytes, word_timestamps
