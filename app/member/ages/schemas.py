from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List


class MemberAgeGroupCreate(BaseModel):
    """创建年龄段"""
    name: str
    sub_id: Optional[int] = None

    class Config:
        orm_mode = True


class MemberAgeGroupUpdate(BaseModel):
    """更新年龄段"""
    name: str

    class Config:
        orm_mode = True


class MemberAgeGroupResponse(BaseModel):
    """年龄段返回"""
    id: int
    name: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class MemberAgeGroupPaginateResponse(BaseModel):
    """年龄段分页返回"""
    total: Optional[int] = None
    pages: Optional[int] = None
    skip: Optional[int] = None
    limit: Optional[int] = None
    data: List[MemberAgeGroupResponse]
