from pydantic import BaseModel

class VideoData(BaseModel):
    id: str | None = None
    category: str = ""
    title: str = ""
    flag: str = "▶️"
    description: str = ""
    videoUrl: str = ""
    flipbookUrl: str = ""
