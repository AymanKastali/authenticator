from pydantic import BaseModel, EmailStr


class SessionLoginRequestSchema(BaseModel):
    email: EmailStr
    password: str
