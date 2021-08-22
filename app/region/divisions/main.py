from fastapi import APIRouter, Depends, Security, HTTPException, status
from sqlalchemy.orm import Session

from .schemas import RegionDivisionCreate, RegionDivisionUpdate, RegionDivisionResponse, \
    RegionDivisionPaginateResponse
from ..defs import verification_sub_id

from ...admin.auth.defs import dbs
from ...admin.auth.oauth import current_user_security
from ...admin.auth.schemas import TokenData

router = APIRouter()

scopes = ['admin']


@router.get('/', response_model=RegionDivisionPaginateResponse)
async def divisions(db: Session = Depends(dbs), user: TokenData = Security(current_user_security, scopes=scopes),
                    skip: int = 0, limit: int = 25):
    """
    获取区域事业部
    :param db:
    :param user:
    :param skip:
    :param limit:
    :return:
    """
    from .crud import get_paginate_divisions
    return get_paginate_divisions(db=db, skip=skip, limit=limit, sub_id=user.sub_id)


@router.post('/', response_model=RegionDivisionResponse)
async def create_division(division: RegionDivisionCreate, db: Session = Depends(dbs),
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
    return create_division(db=db, division=division)


@router.get('/{pk}', response_model=RegionDivisionResponse)
async def get_division(pk: int, db: Session = Depends(dbs),
                       user: TokenData = Security(current_user_security, scopes=scopes)):
    """
    根据pk 获取区域事业部
    :param pk:
    :param db:
    :param user:
    :return:
    """
    from .crud import get_division_by_pk
    db_division = get_division_by_pk(db=db, pk=pk, sub_id=user.sub_id)
    if db_division is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Division not found")
    return db_division


@router.put("/{pk}", response_model=RegionDivisionResponse)
async def update_division(pk: int, division: RegionDivisionUpdate, db: Session = Depends(dbs),
                          user: TokenData = Security(current_user_security, scopes=scopes)):
    """
    根据pk 修改区域事业部内容
    :param pk:
    :param division:
    :param db:
    :param user:
    :return:
    """
    from .crud import update_division, get_division_by_pk
    db_division = get_division_by_pk(db=db, pk=pk, sub_id=user.sub_id)
    if db_division is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Division not found")
    return update_division(db=db, division=division, pk=pk, sub_id=user.sub_id)


@router.delete("/{pk}")
async def delete_division(pk: int, db: Session = Depends(dbs),
                          user: TokenData = Security(current_user_security, scopes=scopes)):
    from .crud import delete_division
    return delete_division(db=db, pk=pk, sub_id=user.sub_id)
