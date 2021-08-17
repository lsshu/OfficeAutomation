from pydantic import BaseModel
from typing import Optional, List


class Token(BaseModel):
    """"""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
    user_id: Optional[int] = 0
    sub_id: Optional[int] = 0
    scopes: List[str] = []


class User(BaseModel):
    username: str
    available: Optional[bool] = None


class AuthUserOut(User):
    password: str
    hashids: str
    sub_hashids: str

    class Config:
        orm_mode = True
