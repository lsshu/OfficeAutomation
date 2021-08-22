from fastapi import APIRouter, Depends, Security, HTTPException, status
from sqlalchemy.orm import Session

from .schemas import RegionMarketCreate, RegionMarketUpdate, RegionMarketResponse, \
    RegionMarketPaginateResponse
from ..defs import verification_sub_id

from ...admin.auth.defs import dbs
from ...admin.auth.oauth import current_user_security
from ...admin.auth.schemas import TokenData

router = APIRouter()

scopes = ['admin']


@router.get('/', response_model=RegionMarketPaginateResponse)
async def markets(db: Session = Depends(dbs), user: TokenData = Security(current_user_security, scopes=scopes),
                  skip: int = 0, limit: int = 25):
    """
    获取区域市场
    :param db:
    :param user:
    :param skip:
    :param limit:
    :return:
    """
    from .crud import get_paginate_markets
    return get_paginate_markets(db=db, skip=skip, limit=limit, sub_id=user.sub_id)


@router.post('/', response_model=RegionMarketResponse)
async def create_market(market: RegionMarketCreate, db: Session = Depends(dbs),
                        user: TokenData = Security(current_user_security, scopes=scopes)):
    """
    创建区域市场
    :param market:
    :param db:
    :param user:
    :return:
    """
    from .crud import create_market, get_market_by_name
    market = verification_sub_id(market, user)
    db_market = get_market_by_name(db=db, name=market.name)
    if db_market:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Market already registered")
    return create_market(db=db, market=market)


@router.get('/{pk}', response_model=RegionMarketResponse)
async def get_market(pk: int, db: Session = Depends(dbs),
                     user: TokenData = Security(current_user_security, scopes=scopes)):
    """
    根据pk 获取区域市场
    :param pk:
    :param db:
    :param user:
    :return:
    """
    from .crud import get_market_by_pk
    db_market = get_market_by_pk(db=db, pk=pk, sub_id=user.sub_id)
    if db_market is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Market not found")
    return db_market


@router.put("/{pk}", response_model=RegionMarketResponse)
async def update_market(pk: int, market: RegionMarketUpdate, db: Session = Depends(dbs),
                        user: TokenData = Security(current_user_security, scopes=scopes)):
    """
    根据pk 修改区域市场内容
    :param pk:
    :param market:
    :param db:
    :param user:
    :return:
    """
    from .crud import update_market, get_market_by_pk
    db_market = get_market_by_pk(db=db, pk=pk, sub_id=user.sub_id)
    if db_market is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Market not found")
    return update_market(db=db, market=market, pk=pk, sub_id=user.sub_id)


@router.delete("/{pk}")
async def delete_market(pk: int, db: Session = Depends(dbs),
                        user: TokenData = Security(current_user_security, scopes=scopes)):
    from .crud import delete_market
    return delete_market(db=db, pk=pk, sub_id=user.sub_id)
