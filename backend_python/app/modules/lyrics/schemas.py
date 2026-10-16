from pydantic import BaseModel

class SongLyricsRequest(BaseModel):
    url: str
