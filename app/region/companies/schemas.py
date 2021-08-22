from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List


class RegionCompanyCreate(BaseModel):
    """创建区域公司"""
    name: str
    sub_id: Optional[int] = None

    class Config:
        orm_mode = True


class RegionCompanyUpdate(BaseModel):
    """更新区域公司"""
    name: str

    class Config:
        orm_mode = True


class RegionCompanyResponse(BaseModel):
    """区域公司返回"""
    id: int
    name: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class RegionCompanyPaginateResponse(BaseModel):
    """区域公司分页返回"""
    total: Optional[int] = None
    pages: Optional[int] = None
    skip: Optional[int] = None
    limit: Optional[int] = None
    data: List[RegionCompanyResponse]
