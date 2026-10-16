from pydantic import BaseModel

class InfoRequest(BaseModel):
    url: str

class DownloadRequest(BaseModel):
    url: str
    type: str  # image, video, audio
    quality: int | str | None = None
    jobId: str | None = None
