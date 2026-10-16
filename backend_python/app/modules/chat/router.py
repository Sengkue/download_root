import httpx
from fastapi import APIRouter, HTTPException

from app.core.config import API_KEYS
from app.modules.chat.schemas import ChatRequest

router = APIRouter(prefix="/chat", tags=["AI Chat"])

current_key_index = 0

SYSTEM_INSTRUCTION = (
    "You are a helpful, friendly AI assistant built into a media downloading app. "
    "Give concise and helpful answers. If the user asks for an image to be generated, created, "
    "or drawn, return exactly this markdown: ![image description](https://image.pollinations.ai/prompt/image_description) "
    "replacing 'image_description' with a detailed prompt of the requested image (URL-encoded). "
    "Do not use markdown code blocks for the image link."
)

MODELS_TO_TRY = ["gemini-2.0-flash", "gemini-1.5-flash", "gemini-2.5-flash", "gemini-flash-latest"]

@router.post("")
@router.post("/")
async def chat(data: ChatRequest):
    global current_key_index

    if not data.messages or not isinstance(data.messages, list):
        raise HTTPException(status_code=400, detail="Messages array is required")

    if not API_KEYS:
        raise HTTPException(status_code=500, detail="AI features are not configured properly.")

    contents = [
        {
            "role": "user" if msg.role == "user" else "model",
            "parts": [{"text": msg.content}]
        }
        for msg in data.messages
    ]

    keys_tried = 0
    last_error = None
    last_status = 500

    async with httpx.AsyncClient(timeout=30.0) as client:
        while keys_tried < len(API_KEYS):
            api_key = API_KEYS[current_key_index]
            for model_name in MODELS_TO_TRY:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
                payload = {
                    "contents": contents,
                    "systemInstruction": {
                        "parts": [{"text": SYSTEM_INSTRUCTION}]
                    }
                }
                try:
                    res = await client.post(url, json=payload)
                    if res.status_code == 200:
                        res_data = res.json()
                        candidates = res_data.get("candidates", [])
                        if candidates:
                            text = "".join(
                                part.get("text", "")
                                for part in candidates[0].get("content", {}).get("parts", [])
                            )
                            return {"message": text}
                    elif res.status_code == 404:
                        continue
                    else:
                        last_status = res.status_code
                        last_error = res.text
                        break
                except Exception as ex:
                    last_error = str(ex)
                    break

            if last_status in [429, 403, 400, 503]:
                current_key_index = (current_key_index + 1) % len(API_KEYS)
                keys_tried += 1
            else:
                break

    error_message = "Failed to communicate with AI"
    if last_status == 429:
        error_message = "The AI is currently receiving too many requests and all backup API keys have hit their rate limit. Please try again later."
    elif last_status in [403, 400]:
        error_message = "All backup API keys have been denied access or are invalid."

    raise HTTPException(status_code=last_status, detail=error_message)
