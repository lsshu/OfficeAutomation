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
async def divisions(db: Session = Depends(dbs), user: TokenData = Security(current_user_security, scopes=scopes),
                  page: int = 1, limit: int = 25, name: str = None):
    """
    获取区域事业部
    :param db:
    :param user:
    :param page:
    :param limit:
    :param name:
    :return:
    """
    from .crud import get_paginate_divisions
    data, count, pages = get_paginate_divisions(db=db, page=page, limit=limit, sub_id=user.sub_id, name=name)
    return {"data": data, "count": count, "pages": pages, "page": page, "limit": limit}


@router.post('/', response_model=StatusResponse)
async def create_division(division: CreateUpdate, db: Session = Depends(dbs),
                        user: TokenData = Security(current_user_security, scopes=scopes)):
    """
    创建区域事业部
    :param division:
    :param db:
    :param user:
    :return:
    """
    from .crud import create_division, get_division_by_name
    division = verification_sub_id(division, user)
    db_division = get_division_by_name(db=db, name=division.name)
    if db_division:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Division already registered")
    create_division(db=db, division=division)
    return StatusResponse()


@router.get('/{sec}', response_model=ModelStatusResponse)
async def get_division(sec: int, db: Session = Depends(dbs),
                     user: TokenData = Security(current_user_security, scopes=scopes)):
    """
    根据sec 获取区域事业部
    :param sec:
    :param db:
    :param user:
    :return:
    """
    from .crud import get_division_by_sec
    db_division = get_division_by_sec(db=db, sec=sec, sub_id=user.sub_id)
    if db_division is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Division not found")
    return ModelStatusResponse(data=db_division)


@router.put("/{sec}", response_model=StatusResponse)
async def update_division(sec: int, division: CreateUpdate, db: Session = Depends(dbs),
                        user: TokenData = Security(current_user_security, scopes=scopes)):
    """
    根据sec 修改区域事业部内容
    :param sec:
    :param division:
    :param db:
    :param user:
    :return:
    """
    from .crud import update_division, get_division_by_sec
    db_division = get_division_by_sec(db=db, sec=sec, sub_id=user.sub_id)
    if db_division is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Division not found")
    update_division(db=db, division=division, sec=sec, sub_id=user.sub_id)
    return StatusResponse()


@router.delete("/", response_model=StatusResponse)
async def delete_division(sec: List[int], db: Session = Depends(dbs),
                        user: TokenData = Security(current_user_security, scopes=scopes)):
    """
    根据sec 删除区域事业部
    :param sec:
    :param db:
    :param user:
    :return:
    """
    from .crud import delete_divisions
    delete_divisions(db=db, sec=sec, sub_id=user.sub_id)
    return StatusResponse()
