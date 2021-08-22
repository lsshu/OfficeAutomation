from sqlalchemy.orm import Session

from .schemas import RegionMarketCreate, RegionMarketUpdate
from ..models import RegionMarket


def get_markets(db: Session, skip: int = 0, limit: int = 10, sub_id=None):
    """
    获取 区域市场列表
    :param db:
    :param skip:
    :param limit:
    :param sub_id:
    :return:
    """
    if sub_id:
        return db.query(RegionMarket).filter(
            RegionMarket.sub_id == sub_id, RegionMarket.deleted_at.is_(None)
        ).offset(skip).limit(limit).all()
    return db.query(RegionMarket).filter(
        RegionMarket.deleted_at.is_(None)
    ).offset(skip).limit(limit).all()


def get_paginate_markets(db: Session, skip: int = 0, limit: int = 10, sub_id=None):
    import math
    if sub_id:
        count = db.query(RegionMarket).filter(
            RegionMarket.sub_id == sub_id, RegionMarket.deleted_at.is_(None)
        ).count()
    else:
        count = db.query(RegionMarket).filter(
            RegionMarket.deleted_at.is_(None)
        ).count()

    pages = math.ceil(count / limit)
    return {"total": count, "pages": pages, "skip": skip, "limit": limit,
            "data": get_markets(db=db, skip=skip, limit=limit, sub_id=sub_id)}


def get_market_by_pk(db: Session, pk: int, sub_id=None):
    """
    根据主键 获取区域市场
    :param db:
    :param pk:
    :param sub_id:
    :return:
    """
    if sub_id:
        return db.query(RegionMarket).filter(
            RegionMarket.sub_id == sub_id, RegionMarket.id == pk, RegionMarket.deleted_at.is_(None)
        ).first()
    return db.query(RegionMarket).filter(
        RegionMarket.id == pk, RegionMarket.deleted_at.is_(None)
    ).first()


def get_market_by_name(db: Session, name: str, sub_id=None):
    """
    根据名称 获取区域市场
    :param db:
    :param name:
    :param sub_id:
    :return:
    """
    if sub_id:
        return db.query(RegionMarket).filter(
            RegionMarket.sub_id == sub_id, RegionMarket.name == name, RegionMarket.deleted_at.is_(None)
        ).first()
    return db.query(RegionMarket).filter(
        RegionMarket.name == name, RegionMarket.deleted_at.is_(None)
    ).first()


def create_market(db: Session, market: RegionMarketCreate, sub_id=None):
    """
    创建 区域市场
    :param db:
    :param market:
    :param sub_id:
    :return:
    """
    db_market = RegionMarket(**market.dict())
    db.add(db_market)
    db.commit()
    db.refresh(db_market)
    return db_market


def update_market(db: Session, market: RegionMarketUpdate, pk: int, sub_id=None):
    """
    修改 区域市场
    :param db:
    :param market:
    :param pk:
    :param sub_id:
    :return:
    """
    if sub_id:
        db.query(RegionMarket).filter(
            RegionMarket.sub_id == sub_id, RegionMarket.id == pk, RegionMarket.deleted_at.is_(None)
        ).update(market.dict()), db.commit(), db.close()
        return get_market_by_pk(db=db, pk=pk, sub_id=sub_id)
    db.query(RegionMarket).filter(
        RegionMarket.id == pk, RegionMarket.deleted_at.is_(None)
    ).update(market.dict()), db.commit(), db.close()
    return get_market_by_pk(db=db, pk=pk, sub_id=sub_id)


def delete_market(db: Session, pk: int, sub_id=None):
    """
    删除区域市场 修改删除时间
    :param db:
    :param pk:
    :param sub_id:
    :return:
    """
    from datetime import datetime
    if sub_id:
        response = db.query(RegionMarket).filter(
            RegionMarket.sub_id == sub_id, RegionMarket.id == pk, RegionMarket.deleted_at.is_(None)
        ).update({"deleted_at": datetime.now()})
        db.commit(), db.close()
        return response
    response = db.query(RegionMarket).filter(
        RegionMarket.id == pk, RegionMarket.deleted_at.is_(None)
    ).update({"deleted_at": datetime.now()})
    db.commit(), db.close()
    return response
