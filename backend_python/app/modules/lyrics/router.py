import re
import urllib.parse
import httpx
from bs4 import BeautifulSoup
from fastapi import APIRouter, HTTPException, Query

from app.modules.lyrics.schemas import SongLyricsRequest

router = APIRouter(prefix="/lyrics", tags=["Lyrics"])

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5"
}

@router.get("/home")
async def get_home_lyrics():
    try:
        async with httpx.AsyncClient(headers=HEADERS, timeout=20.0, follow_redirects=True) as client:
            resp = await client.get("https://hmonglyrics.net/")
            if resp.status_code != 200:
                raise HTTPException(status_code=resp.status_code, detail="Failed to fetch hmonglyrics homepage")

            html = resp.text
            soup = BeautifulSoup(html, "html.parser")

            featured = []
            for el in soup.select("#popular-listr li.gradient"):
                title_el = el.select_one("h3 a")
                artist_el = el.select_one(".item-text > a")
                if not title_el:
                    continue
                title = title_el.get_text(strip=True)
                url = title_el.get("href", "")
                artist = artist_el.get_text(strip=True) if artist_el else ""

                bg_style = el.get("style", "")
                image = ""
                img_match = re.search(r"url\(['\"]?(.*?)['\"]?\)", bg_style)
                if img_match:
                    image = img_match.group(1)

                if title and url:
                    featured.append({"title": title, "artist": artist, "url": url, "image": image})

            latest = []
            for el in soup.select(".latest-lyrics li"):
                title_el = el.select_one("h5 a")
                artist_el = el.select_one(".lyric-content > a")
                if not title_el:
                    continue
                title = title_el.get_text(strip=True)
                url = title_el.get("href", "")
                artist = artist_el.get_text(strip=True) if artist_el else ""

                if title and url:
                    latest.append({"title": title, "artist": artist, "url": url})

            return {"featured": featured, "latest": latest}
    except Exception as e:
        print(f"Lyrics home error: {e}")
        raise HTTPException(status_code=500, detail="Backend failed to proxy the request.")

@router.get("/search")
async def search_lyrics(q: str = Query(None)):
    if not q:
        raise HTTPException(status_code=400, detail="Search query is required")

    try:
        search_url = f"https://hmonglyrics.net/?s={urllib.parse.quote(q)}&post_type=lyrics"
        async with httpx.AsyncClient(headers=HEADERS, timeout=20.0, follow_redirects=True) as client:
            resp = await client.get(search_url)
            if resp.status_code != 200:
                raise HTTPException(status_code=resp.status_code, detail="Failed to search hmonglyrics.net")

            soup = BeautifulSoup(resp.text, "html.parser")
            results = []
            for el in soup.select(".list-line"):
                title_el = el.select_one(".col-lg-6 a")
                artists = el.select(".col-lg-3 a")
                artist_name = "Unknown"
                if artists:
                    artist_name = artists[-1].get_text(strip=True)

                if title_el:
                    results.append({
                        "title": title_el.get_text(strip=True),
                        "url": title_el.get("href", ""),
                        "artist": artist_name
                    })

            return {"results": results}
    except Exception as e:
        print(f"Lyrics search error: {e}")
        raise HTTPException(status_code=500, detail="Failed to search lyrics")

@router.post("/song")
async def get_song_lyrics(data: SongLyricsRequest):
    if not data.url:
        raise HTTPException(status_code=400, detail="Song URL is required")

    try:
        async with httpx.AsyncClient(headers=HEADERS, timeout=20.0, follow_redirects=True) as client:
            resp = await client.get(data.url)
            if resp.status_code != 200:
                raise HTTPException(status_code=resp.status_code, detail="Failed to fetch song from hmonglyrics.net")

            soup = BeautifulSoup(resp.text, "html.parser")
            title_el = soup.select_one(".lyrics-title h1")
            artist_el = soup.select_one(".lyrics-title h3 a")

            title = title_el.get_text(strip=True) if title_el else "Unknown Title"
            artist = artist_el.get_text(strip=True) if artist_el else "Unknown Artist"

            background_image = ""
            bg_div = soup.select_one(".background-single-lyrics")
            if bg_div:
                style = bg_div.get("style", "")
                m = re.search(r"background:\s*url\(([^)]+)\)", style)
                if m:
                    background_image = m.group(1).replace("'", "").replace('"', "")

            video_url = ""
            iframe = soup.select_one(".single-lyric-video iframe")
            if iframe:
                video_url = iframe.get("src", "")

            lyric_div = soup.select_one(".lyric-text")
            clean_text = ""
            if lyric_div:
                for bad in lyric_div.select(".ads, script, ins, .related-list"):
                    bad.decompose()

                for br in lyric_div.find_all("br"):
                    br.replace_with("\n")

                for p in lyric_div.find_all("p"):
                    p.replace_with(p.get_text() + "\n\n")

                raw_text = lyric_div.get_text().strip()
                clean_text = re.sub(r"\n{3,}", "\n\n", raw_text)

            return {
                "title": title,
                "artist": artist,
                "lyrics": clean_text,
                "backgroundImage": background_image,
                "videoUrl": video_url
            }
    except Exception as e:
        print(f"Lyrics fetch error: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch lyrics")
