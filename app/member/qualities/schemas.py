from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List


class MemberQualityTypeCreate(BaseModel):
    """创建粉质量类别"""
    name: str
    sub_id: Optional[int] = None

    class Config:
        orm_mode = True


class MemberQualityTypeUpdate(BaseModel):
    """更新粉质量类别"""
    name: str

    class Config:
        orm_mode = True


class MemberQualityTypeResponse(BaseModel):
    """粉质量类别返回"""
    id: int
    name: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class MemberQualityTypePaginateResponse(BaseModel):
    """粉质量类别分页返回"""
    total: Optional[int] = None
    pages: Optional[int] = None
    skip: Optional[int] = None
    limit: Optional[int] = None
    data: List[MemberQualityTypeResponse]
