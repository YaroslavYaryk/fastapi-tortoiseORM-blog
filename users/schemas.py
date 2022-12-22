from typing import List, Optional
from pydantic import BaseModel


class UserSchema(BaseModel):
    username: str
    email: str
    password: str


class UserLoginSchema(BaseModel):
    email: str
    password: str


class UserRegisteLoginResponse(BaseModel):
    id: str
    email: str
    access: str
