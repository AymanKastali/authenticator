from pydantic import BaseModel, EmailStr


class LoginUserModel(BaseModel):
    email: EmailStr
    password: str
