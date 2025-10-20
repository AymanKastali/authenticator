from pydantic import BaseModel, EmailStr


class LoginUserModel(BaseModel):
    email_address: EmailStr
    password: str
