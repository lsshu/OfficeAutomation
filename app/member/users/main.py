from fastapi import APIRouter, Depends, Security, HTTPException, status
from sqlalchemy.orm import Session

from .schemas import MemberUserCreate, MemberUserUpdate, MemberUserResponse, MemberUserPaginateResponse
from ..defs import verification_sub_id

from ...admin.auth.defs import dbs
from ...admin.auth.oauth import current_user_security
from ...admin.auth.schemas import TokenData

router = APIRouter()

scopes = ['admin']


@router.get('/', response_model=MemberUserPaginateResponse)
async def users(db: Session = Depends(dbs), user: TokenData = Security(current_user_security, scopes=scopes),
                page: int = 1, limit: int = 25):
    """
    获取客户信息
    :param db:
    :param user:
    :param page:
    :param limit:
    :return:
    """
    from .crud import get_paginate_users
    data, count, pages = get_paginate_users(db=db, page=page, limit=limit, sub_id=user.sub_id)
    return {"code": 0, "message": "", "data": data, "count": count, "pages": pages, "page": page, "limit": limit}


@router.post('/', response_model=MemberUserResponse)
async def create_user(user: MemberUserCreate, db: Session = Depends(dbs),
                      auth: TokenData = Security(current_user_security, scopes=scopes)):
    """
    创建客户信息
    :param user:
    :param db:
    :param auth:
    :return:
    """
    from .crud import create_user, get_user_by_name
    user = verification_sub_id(user, auth)
    db_user = get_user_by_name(db=db, name=user.username)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Source already registered")
    return create_user(db=db, user=user, auth=auth)


@router.get('/{pk}', response_model=MemberUserResponse)
async def get_user(pk: int, db: Session = Depends(dbs),
                   user: TokenData = Security(current_user_security, scopes=scopes)):
    """
    根据pk 获取客户信息
    :param pk:
    :param db:
    :param user:
    :return:
    """
    from .crud import get_user_by_pk
    db_user = get_user_by_pk(db=db, pk=pk, sub_id=user.sub_id)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Source not found")
    return db_user


@router.put("/{pk}", response_model=MemberUserResponse)
async def update_user(pk: int, user: MemberUserUpdate, db: Session = Depends(dbs),
                      auth: TokenData = Security(current_user_security, scopes=scopes)):
    """
    根据pk 修改客户信息内容
    :param pk:
    :param user:
    :param db:
    :param auth:
    :return:
    """
    from .crud import update_user, get_user_by_pk
    db_user = get_user_by_pk(db=db, pk=pk, sub_id=auth.sub_id)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Source not found")
    return update_user(db=db, user=user, pk=pk, sub_id=auth.sub_id)


@router.delete("/{pk}")
async def delete_user(pk: int, db: Session = Depends(dbs),
                      user: TokenData = Security(current_user_security, scopes=scopes)):
    from .crud import delete_user
    return delete_user(db=db, pk=pk, sub_id=user.sub_id)
