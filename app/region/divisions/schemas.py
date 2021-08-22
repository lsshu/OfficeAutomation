from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List


class RegionDivisionCreate(BaseModel):
    """创建区域事业部"""
    name: str
    sub_id: Optional[int] = None

    class Config:
        orm_mode = True


class RegionDivisionUpdate(BaseModel):
    """更新区域事业部"""
    name: str

    class Config:
        orm_mode = True


class RegionDivisionResponse(BaseModel):
    """区域事业部返回"""
    id: int
    name: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class RegionDivisionPaginateResponse(BaseModel):
    """区域事业部分页返回"""
    total: Optional[int] = None
    pages: Optional[int] = None
    skip: Optional[int] = None
    limit: Optional[int] = None
    data: List[RegionDivisionResponse]
