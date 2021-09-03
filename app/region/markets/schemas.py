from pydantic import BaseModel
from typing import Optional, List

from app.admin.auth.schemas import StatusResponse


class CreateUpdate(BaseModel):
    """创建区域市场"""
    name: str
    sub_id: Optional[int] = None

    class Config:
        orm_mode = True


class ModelResponse(BaseModel):
    """区域市场返回"""
    from datetime import datetime
    sec_id: int
    name: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class ModelStatusResponse(StatusResponse):
    """区域市场状态返回"""
    data: ModelResponse


class PaginateStatusResponse(StatusResponse):
    """区域市场分页返回"""
    count: Optional[int] = None
    pages: Optional[int] = None
    skip: Optional[int] = None
    limit: Optional[int] = None
    data: List[ModelResponse]
