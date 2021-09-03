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
async def sources(db: Session = Depends(dbs), user: TokenData = Security(current_user_security, scopes=scopes),
                  page: int = 1, limit: int = 25, name: str = None):
    """
    获取添加方式
    :param db:
    :param user:
    :param page:
    :param limit:
    :param name:
    :return:
    """
    from .crud import get_paginate_sources
    data, count, pages = get_paginate_sources(db=db, page=page, limit=limit, sub_id=user.sub_id, name=name)
    return {"data": data, "count": count, "pages": pages, "page": page, "limit": limit}


@router.post('/', response_model=StatusResponse)
async def create_source(source: CreateUpdate, db: Session = Depends(dbs),
                        user: TokenData = Security(current_user_security, scopes=scopes)):
    """
    创建添加方式
    :param source:
    :param db:
    :param user:
    :return:
    """
    from .crud import create_source, get_source_by_name
    source = verification_sub_id(source, user)
    db_source = get_source_by_name(db=db, name=source.name)
    if db_source:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Source already registered")
    create_source(db=db, source=source)
    return StatusResponse()


@router.get('/{sec}', response_model=ModelStatusResponse)
async def get_source(sec: int, db: Session = Depends(dbs),
                     user: TokenData = Security(current_user_security, scopes=scopes)):
    """
    根据sec 获取添加方式
    :param sec:
    :param db:
    :param user:
    :return:
    """
    from .crud import get_source_by_sec
    db_source = get_source_by_sec(db=db, sec=sec, sub_id=user.sub_id)
    if db_source is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Source not found")
    return ModelStatusResponse(data=db_source)


@router.put("/{sec}", response_model=StatusResponse)
async def update_source(sec: int, source: CreateUpdate, db: Session = Depends(dbs),
                        user: TokenData = Security(current_user_security, scopes=scopes)):
    """
    根据sec 修改添加方式内容
    :param sec:
    :param source:
    :param db:
    :param user:
    :return:
    """
    from .crud import update_source, get_source_by_sec
    db_source = get_source_by_sec(db=db, sec=sec, sub_id=user.sub_id)
    if db_source is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Source not found")
    update_source(db=db, source=source, sec=sec, sub_id=user.sub_id)
    return StatusResponse()


@router.delete("/", response_model=StatusResponse)
async def delete_source(sec: List[int], db: Session = Depends(dbs),
                        user: TokenData = Security(current_user_security, scopes=scopes)):
    """
    根据sec 删除添加方式
    :param sec:
    :param db:
    :param user:
    :return:
    """
    from .crud import delete_sources
    delete_sources(db=db, sec=sec, sub_id=user.sub_id)
    return StatusResponse()
