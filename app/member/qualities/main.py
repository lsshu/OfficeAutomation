from fastapi import APIRouter, Depends, Security, HTTPException, status
from sqlalchemy.orm import Session

from .schemas import MemberQualityTypeCreate, MemberQualityTypeUpdate, MemberQualityTypeResponse, \
    MemberQualityTypePaginateResponse
from ..defs import verification_sub_id

from ...admin.auth.defs import dbs
from ...admin.auth.oauth import current_user_security
from ...admin.auth.schemas import TokenData

router = APIRouter()

scopes = ['admin']


@router.get('/', response_model=MemberQualityTypePaginateResponse)
async def quality_types(db: Session = Depends(dbs), user: TokenData = Security(current_user_security, scopes=scopes),
                        skip: int = 0, limit: int = 25):
    """
    获取粉质量类别
    :param db:
    :param user:
    :param skip:
    :param limit:
    :return:
    """
    from .crud import get_paginate_quality_types
    return get_paginate_quality_types(db=db, skip=skip, limit=limit, sub_id=user.sub_id)


@router.post('/', response_model=MemberQualityTypeResponse)
async def create_quality_type(quality_type: MemberQualityTypeCreate, db: Session = Depends(dbs),
                              user: TokenData = Security(current_user_security, scopes=scopes)):
    """
    创建粉质量类别
    :param quality_type:
    :param db:
    :param user:
    :return:
    """
    from .crud import create_quality_type, get_quality_type_by_name
    quality_type = verification_sub_id(quality_type, user)
    db_quality_type = get_quality_type_by_name(db=db, name=quality_type.name)
    if db_quality_type:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="QualityType already registered")
    return create_quality_type(db=db, quality_type=quality_type)


@router.get('/{pk}', response_model=MemberQualityTypeResponse)
async def get_quality_type(pk: int, db: Session = Depends(dbs),
                           user: TokenData = Security(current_user_security, scopes=scopes)):
    """
    根据pk 获取粉质量类别
    :param pk:
    :param db:
    :param user:
    :return:
    """
    from .crud import get_quality_type_by_pk
    db_quality_type = get_quality_type_by_pk(db=db, pk=pk, sub_id=user.sub_id)
    if db_quality_type is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="QualityType not found")
    return db_quality_type


@router.put("/{pk}", response_model=MemberQualityTypeResponse)
async def update_quality_type(pk: int, quality_type: MemberQualityTypeUpdate, db: Session = Depends(dbs),
                              user: TokenData = Security(current_user_security, scopes=scopes)):
    """
    根据pk 修改粉质量类别内容
    :param pk:
    :param quality_type:
    :param db:
    :param user:
    :return:
    """
    from .crud import update_quality_type, get_quality_type_by_pk
    db_quality_type = get_quality_type_by_pk(db=db, pk=pk, sub_id=user.sub_id)
    if db_quality_type is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="QualityType not found")
    return update_quality_type(db=db, quality_type=quality_type, pk=pk, sub_id=user.sub_id)


@router.delete("/{pk}")
async def delete_quality_type(pk: int, db: Session = Depends(dbs),
                              user: TokenData = Security(current_user_security, scopes=scopes)):
    from .crud import delete_quality_type
    return delete_quality_type(db=db, pk=pk, sub_id=user.sub_id)
