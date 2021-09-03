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
async def markets(db: Session = Depends(dbs), user: TokenData = Security(current_user_security, scopes=scopes),
                  page: int = 1, limit: int = 25, name: str = None):
    """
    获取区域市场
    :param db:
    :param user:
    :param page:
    :param limit:
    :param name:
    :return:
    """
    from .crud import get_paginate_markets
    data, count, pages = get_paginate_markets(db=db, page=page, limit=limit, sub_id=user.sub_id, name=name)
    return {"data": data, "count": count, "pages": pages, "page": page, "limit": limit}


@router.post('/', response_model=StatusResponse)
async def create_market(market: CreateUpdate, db: Session = Depends(dbs),
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
    create_market(db=db, market=market)
    return StatusResponse()


@router.get('/{sec}', response_model=ModelStatusResponse)
async def get_market(sec: int, db: Session = Depends(dbs),
                     user: TokenData = Security(current_user_security, scopes=scopes)):
    """
    根据sec 获取区域市场
    :param sec:
    :param db:
    :param user:
    :return:
    """
    from .crud import get_market_by_sec
    db_market = get_market_by_sec(db=db, sec=sec, sub_id=user.sub_id)
    if db_market is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Market not found")
    return ModelStatusResponse(data=db_market)


@router.put("/{sec}", response_model=StatusResponse)
async def update_market(sec: int, market: CreateUpdate, db: Session = Depends(dbs),
                        user: TokenData = Security(current_user_security, scopes=scopes)):
    """
    根据sec 修改区域市场内容
    :param sec:
    :param market:
    :param db:
    :param user:
    :return:
    """
    from .crud import update_market, get_market_by_sec
    db_market = get_market_by_sec(db=db, sec=sec, sub_id=user.sub_id)
    if db_market is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Market not found")
    update_market(db=db, market=market, sec=sec, sub_id=user.sub_id)
    return StatusResponse()


@router.delete("/", response_model=StatusResponse)
async def delete_market(sec: List[int], db: Session = Depends(dbs),
                        user: TokenData = Security(current_user_security, scopes=scopes)):
    """
    根据sec 删除区域市场
    :param sec:
    :param db:
    :param user:
    :return:
    """
    from .crud import delete_markets
    delete_markets(db=db, sec=sec, sub_id=user.sub_id)
    return StatusResponse()
