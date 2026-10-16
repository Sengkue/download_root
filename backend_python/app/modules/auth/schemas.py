from pydantic import BaseModel

class RegisterRequest(BaseModel):
    username: str
    password: str
    name: str | None = None
    gender: str | None = None
    location: str | None = None

class LoginRequest(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    name: str | None = None
    profileImage: str | None = None
