from fastapi import APIRouter, Depends, Security, HTTPException, status
from sqlalchemy.orm import Session

from .schemas import RegionCompanyCreate, RegionCompanyUpdate, RegionCompanyResponse, \
    RegionCompanyPaginateResponse
from ..defs import verification_sub_id

from ...admin.auth.defs import dbs
from ...admin.auth.oauth import current_user_security
from ...admin.auth.schemas import TokenData

router = APIRouter()

scopes = ['admin']


@router.get('/', response_model=RegionCompanyPaginateResponse)
async def companies(db: Session = Depends(dbs), user: TokenData = Security(current_user_security, scopes=scopes),
                    skip: int = 0, limit: int = 25):
    """
    获取区域公司
    :param db:
    :param user:
    :param skip:
    :param limit:
    :return:
    """
    from .crud import get_paginate_companies
    return get_paginate_companies(db=db, skip=skip, limit=limit, sub_id=user.sub_id)


@router.post('/', response_model=RegionCompanyResponse)
async def create_company(company: RegionCompanyCreate, db: Session = Depends(dbs),
                         user: TokenData = Security(current_user_security, scopes=scopes)):
    """
    创建区域公司
    :param company:
    :param db:
    :param user:
    :return:
    """
    from .crud import create_company, get_company_by_name
    company = verification_sub_id(company, user)
    db_company = get_company_by_name(db=db, name=company.name)
    if db_company:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Company already registered")
    return create_company(db=db, company=company)


@router.get('/{pk}', response_model=RegionCompanyResponse)
async def get_company(pk: int, db: Session = Depends(dbs),
                      user: TokenData = Security(current_user_security, scopes=scopes)):
    """
    根据pk 获取区域公司
    :param pk:
    :param db:
    :param user:
    :return:
    """
    from .crud import get_company_by_pk
    db_company = get_company_by_pk(db=db, pk=pk, sub_id=user.sub_id)
    if db_company is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")
    return db_company


@router.put("/{pk}", response_model=RegionCompanyResponse)
async def update_company(pk: int, company: RegionCompanyUpdate, db: Session = Depends(dbs),
                         user: TokenData = Security(current_user_security, scopes=scopes)):
    """
    根据pk 修改区域公司内容
    :param pk:
    :param company:
    :param db:
    :param user:
    :return:
    """
    from .crud import update_company, get_company_by_pk
    db_company = get_company_by_pk(db=db, pk=pk, sub_id=user.sub_id)
    if db_company is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")
    return update_company(db=db, company=company, pk=pk, sub_id=user.sub_id)


@router.delete("/{pk}")
async def delete_company(pk: int, db: Session = Depends(dbs),
                         user: TokenData = Security(current_user_security, scopes=scopes)):
    from .crud import delete_company
    return delete_company(db=db, pk=pk, sub_id=user.sub_id)
