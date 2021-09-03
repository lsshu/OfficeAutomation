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
async def ages(db: Session = Depends(dbs), user: TokenData = Security(current_user_security, scopes=scopes),
               page: int = 1, limit: int = 25, name: str = None):
    """
    获取年龄段
    :param db:
    :param user:
    :param page:
    :param limit:
    :param name:
    :return:
    """
    from .crud import get_paginate_ages
    data, count, pages = get_paginate_ages(db=db, page=page, limit=limit, sub_id=user.sub_id, name=name)
    return {"data": data, "count": count, "pages": pages, "page": page, "limit": limit}


@router.post('/', response_model=StatusResponse)
async def create_age(age: CreateUpdate, db: Session = Depends(dbs),
                     user: TokenData = Security(current_user_security, scopes=scopes)):
    """
    创建年龄段
    :param age:
    :param db:
    :param user:
    :return:
    """
    from .crud import create_age, get_age_by_name
    age = verification_sub_id(age, user)
    db_age = get_age_by_name(db=db, name=age.name)
    if db_age:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Age already registered")
    create_age(db=db, age=age)
    return StatusResponse()


@router.get('/{sec}', response_model=ModelStatusResponse)
async def get_age(sec: int, db: Session = Depends(dbs),
                  user: TokenData = Security(current_user_security, scopes=scopes)):
    """
    根据sec 获取年龄段
    :param sec:
    :param db:
    :param user:
    :return:
    """
    from .crud import get_age_by_sec
    db_age = get_age_by_sec(db=db, sec=sec, sub_id=user.sub_id)
    if db_age is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Age not found")
    return ModelStatusResponse(data=db_age)


@router.put("/{sec}", response_model=StatusResponse)
async def update_age(sec: int, age: CreateUpdate, db: Session = Depends(dbs),
                     user: TokenData = Security(current_user_security, scopes=scopes)):
    """
    根据sec 修改年龄段内容
    :param sec:
    :param age:
    :param db:
    :param user:
    :return:
    """
    from .crud import update_age, get_age_by_sec
    db_age = get_age_by_sec(db=db, sec=sec, sub_id=user.sub_id)
    if db_age is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Age not found")
    update_age(db=db, age=age, sec=sec, sub_id=user.sub_id)
    return StatusResponse()


@router.delete("/", response_model=StatusResponse)
async def delete_age(sec: List[int], db: Session = Depends(dbs),
                     user: TokenData = Security(current_user_security, scopes=scopes)):
    """
    根据sec 删除年龄段
    :param sec:
    :param db:
    :param user:
    :return:
    """
    from .crud import delete_ages
    delete_ages(db=db, sec=sec, sub_id=user.sub_id)
    return StatusResponse()
