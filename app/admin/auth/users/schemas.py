from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List

from ..schemas import StatusResponse


class AuthUserCreate(BaseModel):
    """创建授权用户"""
    username: str
    password: str
    sub_id: Optional[int] = None
    available: Optional[bool] = True

    class Config:
        orm_mode = True


class AuthUserUpdate(BaseModel):
    """更新授权用户"""
    username: str
    password: str
    available: bool

    class Config:
        orm_mode = True


class AuthUserPatch(BaseModel):
    """更新授权用户"""
    username: Optional[str] = None
    password: Optional[str] = None
    available: Optional[bool] = None

    class Config:
        orm_mode = True


class AuthUserResponse(BaseModel):
    """授权用户返回"""
    sec_id: int
    username: str
    available: bool
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class AuthUserPaginateResponse(StatusResponse):
    """授权用户分页返回"""
    total: Optional[int] = None
    pages: Optional[int] = None
    skip: Optional[int] = None
    limit: Optional[int] = None
    data: List[AuthUserResponse]
