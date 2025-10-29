from pydantic import BaseModel, EmailStr


class LoginUserInDto(BaseModel):
    email: EmailStr
    password: str
