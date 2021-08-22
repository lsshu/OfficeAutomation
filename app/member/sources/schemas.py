from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List


class MemberSourceCreate(BaseModel):
    """创建添加方式"""
    name: str
    sub_id: Optional[int] = None

    class Config:
        orm_mode = True


class MemberSourceUpdate(BaseModel):
    """更新添加方式"""
    name: str

    class Config:
        orm_mode = True


class MemberSourceResponse(BaseModel):
    """添加方式返回"""
    id: int
    name: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class MemberSourcePaginateResponse(BaseModel):
    """添加方式分页返回"""
    total: Optional[int] = None
    pages: Optional[int] = None
    skip: Optional[int] = None
    limit: Optional[int] = None
    data: List[MemberSourceResponse]
