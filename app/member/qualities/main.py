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
async def quality_types(db: Session = Depends(dbs), user: TokenData = Security(current_user_security, scopes=scopes),
                        page: int = 1, limit: int = 25, name: str = None):
    """
    获取加粉质量
    :param db:
    :param user:
    :param page:
    :param limit:
    :param name:
    :return:
    """
    from .crud import get_paginate_quality_types
    data, count, pages = get_paginate_quality_types(db=db, page=page, limit=limit, sub_id=user.sub_id, name=name)
    return {"data": data, "count": count, "pages": pages, "page": page, "limit": limit}


@router.post('/', response_model=StatusResponse)
async def create_quality_type(quality_type: CreateUpdate, db: Session = Depends(dbs),
                              user: TokenData = Security(current_user_security, scopes=scopes)):
    """
    创建加粉质量
    :param quality_type:
    :param db:
    :param user:
    :return:
    """
    from .crud import create_quality_type, get_quality_type_by_name
    quality_type = verification_sub_id(quality_type, user)
    db_quality_type = get_quality_type_by_name(db=db, name=quality_type.name)
    if db_quality_type:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Quality already registered")
    create_quality_type(db=db, quality_type=quality_type)
    return StatusResponse()


@router.get('/{sec}', response_model=ModelStatusResponse)
async def get_quality_type(sec: int, db: Session = Depends(dbs),
                           user: TokenData = Security(current_user_security, scopes=scopes)):
    """
    根据sec 获取加粉质量
    :param sec:
    :param db:
    :param user:
    :return:
    """
    from .crud import get_quality_type_by_sec
    db_quality_type = get_quality_type_by_sec(db=db, sec=sec, sub_id=user.sub_id)
    if db_quality_type is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quality not found")
    return ModelStatusResponse(data=db_quality_type)


@router.put("/{sec}", response_model=StatusResponse)
async def update_quality_type(sec: int, quality_type: CreateUpdate, db: Session = Depends(dbs),
                              user: TokenData = Security(current_user_security, scopes=scopes)):
    """
    根据sec 修改加粉质量内容
    :param sec:
    :param quality_type:
    :param db:
    :param user:
    :return:
    """
    from .crud import update_quality_type, get_quality_type_by_sec
    db_quality_type = get_quality_type_by_sec(db=db, sec=sec, sub_id=user.sub_id)
    if db_quality_type is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quality not found")
    update_quality_type(db=db, quality_type=quality_type, sec=sec, sub_id=user.sub_id)
    return StatusResponse()


@router.delete("/", response_model=StatusResponse)
async def delete_quality_type(sec: List[int], db: Session = Depends(dbs),
                              user: TokenData = Security(current_user_security, scopes=scopes)):
    """
    根据sec 删除加粉质量
    :param sec:
    :param db:
    :param user:
    :return:
    """
    from .crud import delete_quality_types
    delete_quality_types(db=db, sec=sec, sub_id=user.sub_id)
    return StatusResponse()
