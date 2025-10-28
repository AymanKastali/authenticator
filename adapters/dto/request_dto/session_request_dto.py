from pydantic import BaseModel, EmailStr


class SessionLoginInDto(BaseModel):
    email: EmailStr
    password: str
