from fastapi import APIRouter, Depends, Security, HTTPException, status
from sqlalchemy.orm import Session

from .schemas import MemberSourceCreate, MemberSourceUpdate, MemberSourceResponse, MemberSourcePaginateResponse
from ..defs import verification_sub_id

from ...admin.auth.defs import dbs
from ...admin.auth.oauth import current_user_security
from ...admin.auth.schemas import TokenData

router = APIRouter()

scopes = ['admin']


@router.get('/', response_model=MemberSourcePaginateResponse)
async def sources(db: Session = Depends(dbs), user: TokenData = Security(current_user_security, scopes=scopes),
                  skip: int = 0, limit: int = 25):
    """
    获取添加方式
    :param db:
    :param user:
    :param skip:
    :param limit:
    :return:
    """
    from .crud import get_paginate_sources
    return get_paginate_sources(db=db, skip=skip, limit=limit, sub_id=user.sub_id)


@router.post('/', response_model=MemberSourceResponse)
async def create_source(source: MemberSourceCreate, db: Session = Depends(dbs),
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
    return create_source(db=db, source=source)


@router.get('/{pk}', response_model=MemberSourceResponse)
async def get_source(pk: int, db: Session = Depends(dbs),
                     user: TokenData = Security(current_user_security, scopes=scopes)):
    """
    根据pk 获取添加方式
    :param pk:
    :param db:
    :param user:
    :return:
    """
    from .crud import get_source_by_pk
    db_source = get_source_by_pk(db=db, pk=pk, sub_id=user.sub_id)
    if db_source is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Source not found")
    return db_source


@router.put("/{pk}", response_model=MemberSourceResponse)
async def update_source(pk: int, source: MemberSourceUpdate, db: Session = Depends(dbs),
                        user: TokenData = Security(current_user_security, scopes=scopes)):
    """
    根据pk 修改添加方式内容
    :param pk:
    :param source:
    :param db:
    :param user:
    :return:
    """
    from .crud import update_source, get_source_by_pk
    db_source = get_source_by_pk(db=db, pk=pk, sub_id=user.sub_id)
    if db_source is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Source not found")
    return update_source(db=db, source=source, pk=pk, sub_id=user.sub_id)


@router.delete("/{pk}")
async def delete_source(pk: int, db: Session = Depends(dbs),
                        user: TokenData = Security(current_user_security, scopes=scopes)):
    from .crud import delete_source
    return delete_source(db=db, pk=pk, sub_id=user.sub_id)
