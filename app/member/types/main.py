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
async def types(db: Session = Depends(dbs), user: TokenData = Security(current_user_security, scopes=scopes),
                page: int = 1, limit: int = 25, name: str = None):
    """
    获取加粉类别
    :param db:
    :param user:
    :param page:
    :param limit:
    :param name:
    :return:
    """
    from .crud import get_paginate_types
    data, count, pages = get_paginate_types(db=db, page=page, limit=limit, sub_id=user.sub_id, name=name)
    return {"data": data, "count": count, "pages": pages, "page": page, "limit": limit}


@router.post('/', response_model=StatusResponse)
async def create_type(type: CreateUpdate, db: Session = Depends(dbs),
                      user: TokenData = Security(current_user_security, scopes=scopes)):
    """
    创建加粉类别
    :param type:
    :param db:
    :param user:
    :return:
    """
    from .crud import create_type, get_type_by_name
    type = verification_sub_id(type, user)
    db_type = get_type_by_name(db=db, name=type.name)
    if db_type:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Type already registered")
    create_type(db=db, type=type)
    return StatusResponse()


@router.get('/{sec}', response_model=ModelStatusResponse)
async def get_type(sec: int, db: Session = Depends(dbs),
                   user: TokenData = Security(current_user_security, scopes=scopes)):
    """
    根据sec 获取加粉类别
    :param sec:
    :param db:
    :param user:
    :return:
    """
    from .crud import get_type_by_sec
    db_type = get_type_by_sec(db=db, sec=sec, sub_id=user.sub_id)
    if db_type is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Type not found")
    return ModelStatusResponse(data=db_type)


@router.put("/{sec}", response_model=StatusResponse)
async def update_type(sec: int, type: CreateUpdate, db: Session = Depends(dbs),
                      user: TokenData = Security(current_user_security, scopes=scopes)):
    """
    根据sec 修改加粉类别内容
    :param sec:
    :param type:
    :param db:
    :param user:
    :return:
    """
    from .crud import update_type, get_type_by_sec
    db_type = get_type_by_sec(db=db, sec=sec, sub_id=user.sub_id)
    if db_type is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Type not found")
    update_type(db=db, type=type, sec=sec, sub_id=user.sub_id)
    return StatusResponse()


@router.delete("/", response_model=StatusResponse)
async def delete_type(sec: List[int], db: Session = Depends(dbs),
                      user: TokenData = Security(current_user_security, scopes=scopes)):
    """
    根据sec 删除加粉类别
    :param sec:
    :param db:
    :param user:
    :return:
    """
    from .crud import delete_types
    delete_types(db=db, sec=sec, sub_id=user.sub_id)
    return StatusResponse()
