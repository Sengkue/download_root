from pydantic import BaseModel

class CreateLessonRequest(BaseModel):
    title: str
    content: str

class TypingResultRequest(BaseModel):
    username: str = None
    lessonTitle: str
    cpm: int = 0
    wpm: int = 0
    accuracy: float = 0.0
    timeSeconds: str = None

class SaveHistoryRequest(BaseModel):
    lessonTitle: str
    wpm: int = 0
    cpm: int = 0
    accuracy: float = 0.0
    timeSeconds: str = None
