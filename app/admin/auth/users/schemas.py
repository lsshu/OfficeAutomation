from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List


class AuthUserCreate(BaseModel):
    """创建授权用户"""
    name: str
    sub_id: Optional[int] = None

    class Config:
        orm_mode = True


class AuthUserUpdate(BaseModel):
    """更新授权用户"""
    name: str

    class Config:
        orm_mode = True


class AuthUserResponse(BaseModel):
    """授权用户返回"""
    id: int
    name: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class AuthUserPaginateResponse(BaseModel):
    """授权用户分页返回"""
    total: Optional[int] = None
    pages: Optional[int] = None
    skip: Optional[int] = None
    limit: Optional[int] = None
    data: List[AuthUserResponse]
