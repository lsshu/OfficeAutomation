from pydantic import BaseModel
from typing import Optional, List, Union


class StatusResponse(BaseModel):
    """状态返回"""
    code: Optional[int] = 0
    message: Optional[str] = "success"


class Token(StatusResponse):
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


class AuthSubjects(BaseModel):
    """
    主体对象
    """
    name: str
    domain: str
    available: bool

    # expires_time:

    class Config:
        orm_mode = True


class AuthUserMe(BaseModel):
    sec_id: int
    username: str
    available: Optional[bool] = None

    class Config:
        orm_mode = True


class AuthUserMeStatusResponse(StatusResponse):
    data: AuthUserMe
