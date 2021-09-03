from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional, List

from ..ages.schemas import ModelResponse as AgeModelResponse
from ..qualities.schemas import ModelResponse as QualityModelResponse
from ..sources.schemas import ModelResponse as SourcesModelResponse
from ..types.schemas import ModelResponse as TypeModelResponse
from ...admin.auth.schemas import StatusResponse
from ...admin.auth.users.schemas import AuthUserResponse
from ...region.companies.schemas import ModelResponse as CompanyModelResponse
from ...region.divisions.schemas import ModelResponse as DivisionModelResponse
from ...region.markets.schemas import ModelResponse as MarketModelResponse


class MemberUserCreate(BaseModel):
    """创建客户信息"""
    from enum import Enum
    class choice_gender(str, Enum):
        alexnet = "alexnet"
        resnet = "resnet"
        lenet = "lenet"

    sub_id: Optional[int] = None
    com_id: int
    div_id: int
    mar_id: int

    age_id: Optional[int] = None
    sou_id: Optional[int] = None
    qua_id: Optional[int] = None

    own_wx: Optional[str] = Field(None, max_length=15)
    username: Optional[str] = Field(None, max_length=15)
    telephone: Optional[str] = Field(None, max_length=11)
    wx_number: Optional[str] = Field(None, max_length=30)
    wx_nickname: Optional[str] = Field(None, max_length=20)
    gender: Optional[choice_gender]
    asc_province: Optional[int] = None
    asc_city: Optional[int] = None
    pass_at: Optional[datetime] = None
    tra_status: Optional[str] = Field(None, max_length=1)

    class Config:
        orm_mode = True


class MemberUserUpdate(BaseModel):
    """更新客户信息"""
    com_id: int
    div_id: int
    mar_id: int

    age_id: Optional[int] = None
    sou_id: Optional[int] = None
    qua_id: Optional[int] = None

    own_wx: Optional[str] = Field(None, max_length=15)
    username: Optional[str] = Field(None, max_length=15)
    telephone: Optional[str] = Field(None, max_length=11)
    wx_number: Optional[str] = Field(None, max_length=30)
    wx_nickname: Optional[str] = Field(None, max_length=20)
    gender: Optional[str] = Field(None, max_length=1)
    asc_province: Optional[int] = None
    asc_city: Optional[int] = None
    pass_at: Optional[datetime] = None
    tra_status: Optional[str] = Field(None, max_length=1)

    class Config:
        orm_mode = True


class MemberUserResponse(BaseModel):
    """客户信息返回"""
    sec_id: int
    com_id: int
    company: CompanyModelResponse
    div_id: int
    division: DivisionModelResponse
    mar_id: int
    market: MarketModelResponse
    own_id: int
    owner: AuthUserResponse

    age_id: Optional[int] = None
    age: Optional[AgeModelResponse] = None
    sou_id: Optional[int] = None
    source: Optional[SourcesModelResponse] = None
    qua_id: Optional[int] = None
    quality: Optional[QualityModelResponse] = None
    typ_id: Optional[int] = None
    type: Optional[TypeModelResponse] = None

    own_wx: Optional[str] = Field(None, max_length=15)
    username: Optional[str] = Field(None, max_length=15)
    telephone: Optional[str] = Field(None, max_length=11)
    wx_number: Optional[str] = Field(None, max_length=30)
    wx_nickname: Optional[str] = Field(None, max_length=20)
    gender: Optional[str] = Field(None, max_length=1)
    asc_province: Optional[int] = None
    asc_city: Optional[int] = None
    pass_at: Optional[datetime] = None
    tra_status: Optional[str] = Field(None, max_length=1)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class MemberUserPaginateResponse(StatusResponse):
    """客户信息分页返回"""
    count: Optional[int] = None
    pages: Optional[int] = None
    page: Optional[int] = None
    limit: Optional[int] = None
    data: List[MemberUserResponse]
