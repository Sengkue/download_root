from pydantic import BaseModel

class LinkRequest(BaseModel):
    title: str
    url: str
