import urllib.parse
import httpx
from fastapi import APIRouter, HTTPException, Query

router = APIRouter(prefix="/api/search", tags=["Search Proxy"])

@router.get("")
async def search_images(
    key: str = Query(None),
    q: str = Query(None),
    image_type: str = Query("photo"),
    per_page: int = Query(30),
    page: int = Query(1),
    video: str = Query("false")
):
    if not key or not q:
        raise HTTPException(status_code=400, detail="Pixabay API key and search query are required.")

    encoded_q = urllib.parse.quote(q)
    if video == "true":
        url = f"https://pixabay.com/api/videos/?key={key}&q={encoded_q}&per_page={per_page}&page={page}"
    else:
        url = f"https://pixabay.com/api/?key={key}&q={encoded_q}&image_type={image_type}&per_page={per_page}&page={page}"

    async with httpx.AsyncClient(timeout=20.0) as client:
        try:
            res = await client.get(url)
            if res.status_code != 200:
                raise HTTPException(status_code=res.status_code, detail=f"Pixabay API Connection Error: {res.text}")
            return res.json()
        except httpx.RequestError as e:
            raise HTTPException(status_code=500, detail=f"Backend failed to proxy the search request to Pixabay: {str(e)}")
