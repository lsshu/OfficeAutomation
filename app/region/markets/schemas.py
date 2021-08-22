from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List


class RegionMarketCreate(BaseModel):
    """创建区域市场"""
    name: str
    sub_id: Optional[int] = None

    class Config:
        orm_mode = True


class RegionMarketUpdate(BaseModel):
    """更新区域市场"""
    name: str

    class Config:
        orm_mode = True


class RegionMarketResponse(BaseModel):
    """区域市场返回"""
    id: int
    name: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class RegionMarketPaginateResponse(BaseModel):
    """区域市场分页返回"""
    total: Optional[int] = None
    pages: Optional[int] = None
    skip: Optional[int] = None
    limit: Optional[int] = None
    data: List[RegionMarketResponse]
