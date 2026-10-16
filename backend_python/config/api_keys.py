import os
from dotenv import load_dotenv

load_dotenv()

raw_keys = [
    os.getenv("GEMINI_API_KEY", "")
]

API_KEYS = [k.strip() for k in raw_keys if k and k.strip() and "YOUR_API_KEY" not in k]
