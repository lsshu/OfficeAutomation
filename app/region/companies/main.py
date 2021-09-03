from typing import List

from fastapi import APIRouter, Depends, Security, HTTPException, status
from sqlalchemy.orm import Session

from .schemas import StatusResponse, CreateUpdate, ModelStatusResponse, PaginateStatusResponse
from ..defs import verification_sub_id

from ...admin.auth.defs import dbs
from ...admin.auth.oauth import current_user_security
from ...admin.auth.schemas import TokenData

router = APIRouter()

scopes = ['admin']


@router.get('/', response_model=PaginateStatusResponse)
async def companies(db: Session = Depends(dbs), user: TokenData = Security(current_user_security, scopes=scopes),
                    page: int = 1, limit: int = 25, name: str = None):
    """
    获取区域公司
    :param db:
    :param user:
    :param page:
    :param limit:
    :param name:
    :return:
    """
    from .crud import get_paginate_companies
    data, count, pages = get_paginate_companies(db=db, page=page, limit=limit, sub_id=user.sub_id, name=name)
    return {"data": data, "count": count, "pages": pages, "page": page, "limit": limit}


@router.post('/', response_model=StatusResponse)
async def create_company(company: CreateUpdate, db: Session = Depends(dbs),
                         user: TokenData = Security(current_user_security, scopes=scopes)):
    """
    创建区域公司
    :param company:
    :param db:
    :param user:
    :return:
    """
    from .crud import create_company, get_company_by_name
    company = verification_sub_id(company, user)
    db_company = get_company_by_name(db=db, name=company.name)
    if db_company:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Company already registered")
    create_company(db=db, company=company)
    return StatusResponse()


@router.get('/{sec}', response_model=ModelStatusResponse)
async def get_company(sec: int, db: Session = Depends(dbs),
                      user: TokenData = Security(current_user_security, scopes=scopes)):
    """
    根据sec 获取区域公司
    :param sec:
    :param db:
    :param user:
    :return:
    """
    from .crud import get_company_by_sec
    db_company = get_company_by_sec(db=db, sec=sec, sub_id=user.sub_id)
    if db_company is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")
    return ModelStatusResponse(data=db_company)


@router.put("/{sec}", response_model=StatusResponse)
async def update_company(sec: int, company: CreateUpdate, db: Session = Depends(dbs),
                         user: TokenData = Security(current_user_security, scopes=scopes)):
    """
    根据sec 修改区域公司内容
    :param sec:
    :param company:
    :param db:
    :param user:
    :return:
    """
    from .crud import update_company, get_company_by_sec
    db_company = get_company_by_sec(db=db, sec=sec, sub_id=user.sub_id)
    if db_company is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")
    update_company(db=db, company=company, sec=sec, sub_id=user.sub_id)
    return StatusResponse()


@router.delete("/", response_model=StatusResponse)
async def delete_company(sec: List[int], db: Session = Depends(dbs),
                         user: TokenData = Security(current_user_security, scopes=scopes)):
    """
    根据sec 删除区域公司
    :param sec:
    :param db:
    :param user:
    :return:
    """
    from .crud import delete_companies
    delete_companies(db=db, sec=sec, sub_id=user.sub_id)
    return StatusResponse()
