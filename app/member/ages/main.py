from fastapi import APIRouter, Depends, Security, HTTPException, status
from sqlalchemy.orm import Session

from .schemas import MemberAgeGroupCreate, MemberAgeGroupUpdate, MemberAgeGroupResponse, MemberAgeGroupPaginateResponse
from ..defs import verification_sub_id

from ...admin.auth.defs import dbs
from ...admin.auth.oauth import current_user_security
from ...admin.auth.schemas import TokenData

router = APIRouter()

scopes = ['admin']


@router.get('/', response_model=MemberAgeGroupPaginateResponse)
async def ages(db: Session = Depends(dbs), user: TokenData = Security(current_user_security, scopes=scopes),
               skip: int = 0, limit: int = 25):
    """
    获取年龄段
    :param db:
    :param user:
    :param skip:
    :param limit:
    :return:
    """
    from .crud import get_paginate_ages
    return get_paginate_ages(db=db, skip=skip, limit=limit, sub_id=user.sub_id)


@router.post('/', response_model=MemberAgeGroupResponse)
async def create_age(age: MemberAgeGroupCreate, db: Session = Depends(dbs),
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
    return create_age(db=db, age=age)


@router.get('/{pk}', response_model=MemberAgeGroupResponse)
async def get_age(pk: int, db: Session = Depends(dbs),
                  user: TokenData = Security(current_user_security, scopes=scopes)):
    """
    根据pk 获取年龄段
    :param pk:
    :param db:
    :param user:
    :return:
    """
    from .crud import get_age_by_pk
    db_age = get_age_by_pk(db=db, pk=pk, sub_id=user.sub_id)
    if db_age is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Age not found")
    return db_age


@router.put("/{pk}", response_model=MemberAgeGroupResponse)
async def update_age(pk: int, age: MemberAgeGroupUpdate, db: Session = Depends(dbs),
                     user: TokenData = Security(current_user_security, scopes=scopes)):
    """
    根据pk 修改年龄段内容
    :param pk:
    :param age:
    :param db:
    :param user:
    :return:
    """
    from .crud import update_age, get_age_by_pk
    db_age = get_age_by_pk(db=db, pk=pk, sub_id=user.sub_id)
    if db_age is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Age not found")
    return update_age(db=db, age=age, pk=pk, sub_id=user.sub_id)


@router.delete("/{pk}")
async def delete_age(pk: int, db: Session = Depends(dbs),
                     user: TokenData = Security(current_user_security, scopes=scopes)):
    """
    根据pk 删除年龄段
    :param pk:
    :param db:
    :param user:
    :return:
    """
    from .crud import delete_age
    return delete_age(db=db, pk=pk, sub_id=user.sub_id)
