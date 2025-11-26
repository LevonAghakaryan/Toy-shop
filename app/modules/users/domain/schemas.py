from pydantic import BaseModel, Field, EmailStr
from typing import Optional

# Բազային սխեմա
class UserBase(BaseModel):
    email: EmailStr
    username: str = Field(min_length=3, max_length=50)
    role: str = "user"

# Գրանցման սխեմա
class UserCreate(UserBase):
    password: str = Field(min_length=6)

# Մուտքի սխեմա
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Պատասխանի սխեմա (առանց գաղտնաբառի)
class User(UserBase):
    id: int

    class Config:
        from_attributes = True