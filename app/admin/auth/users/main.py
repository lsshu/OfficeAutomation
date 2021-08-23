from fastapi import APIRouter, Depends, Security, HTTPException, status
from sqlalchemy.orm import Session

from .schemas import AuthUserCreate, AuthUserUpdate, AuthUserResponse, AuthUserPaginateResponse
from ..defs import verification_sub_id

from ..defs import dbs
from ..oauth import current_user_security
from ..schemas import TokenData

router = APIRouter()

scopes = ['admin']


@router.get('/', response_model=AuthUserPaginateResponse)
async def auth_users(db: Session = Depends(dbs), user: TokenData = Security(current_user_security, scopes=scopes),
                     skip: int = 0, limit: int = 25):
    """
    获取授权用户
    :param db:
    :param user:
    :param skip:
    :param limit:
    :return:
    """
    from .crud import get_paginate_auth_users
    return get_paginate_auth_users(db=db, skip=skip, limit=limit, sub_id=user.sub_id)


@router.post('/', response_model=AuthUserResponse)
async def create_auth_user(auth_user: AuthUserCreate, db: Session = Depends(dbs),
                           user: TokenData = Security(current_user_security, scopes=scopes)):
    """
    创建授权用户
    :param auth_user:
    :param db:
    :param user:
    :return:
    """
    from .crud import create_auth_user, get_auth_user_by_name
    auth_user = verification_sub_id(auth_user, user)
    db_auth_user = get_auth_user_by_name(db=db, name=auth_user.name)
    if db_auth_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Age already registered")
    return create_auth_user(db=db, auth_user=auth_user)


@router.get('/{pk}', response_model=AuthUserResponse)
async def get_auth_user(pk: int, db: Session = Depends(dbs),
                        user: TokenData = Security(current_user_security, scopes=scopes)):
    """
    根据pk 获取授权用户
    :param pk:
    :param db:
    :param user:
    :return:
    """
    from .crud import get_auth_user_by_pk
    db_auth_user = get_auth_user_by_pk(db=db, pk=pk, sub_id=user.sub_id)
    if db_auth_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Age not found")
    return db_auth_user


@router.put("/{pk}", response_model=AuthUserResponse)
async def update_auth_user(pk: int, auth_user: AuthUserUpdate, db: Session = Depends(dbs),
                           user: TokenData = Security(current_user_security, scopes=scopes)):
    """
    根据pk 修改授权用户内容
    :param pk:
    :param auth_user:
    :param db:
    :param user:
    :return:
    """
    from .crud import update_auth_user, get_auth_user_by_pk
    db_auth_user = get_auth_user_by_pk(db=db, pk=pk, sub_id=user.sub_id)
    if db_auth_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Age not found")
    return update_auth_user(db=db, auth_user=auth_user, pk=pk, sub_id=user.sub_id)


@router.delete("/{pk}")
async def delete_auth_user(pk: int, db: Session = Depends(dbs),
                           user: TokenData = Security(current_user_security, scopes=scopes)):
    """
    根据pk 删除授权用户
    :param pk:
    :param db:
    :param user:
    :return:
    """
    from .crud import delete_auth_user
    return delete_auth_user(db=db, pk=pk, sub_id=user.sub_id)
