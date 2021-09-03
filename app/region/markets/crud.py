from sqlalchemy.orm import Session

from .schemas import CreateUpdate
from ..models import RegionMarket


def get_markets(db: Session, page: int = 1, limit: int = 10, sub_id=None, name=None):
    """
    获取 区域市场列表
    :param db:
    :param page:
    :param limit:
    :param sub_id:
    :param name:
    :return:
    """
    skip = (page - 1) * limit
    q = db.query(RegionMarket)
    if name:
        q = q.filter(RegionMarket.name.like("%" + name + "%"))
    return q.filter(
        RegionMarket.sub_id == sub_id, RegionMarket.deleted_at.is_(None)
    ).offset(skip).limit(limit).all()


def get_model_sec(db: Session, sub_id):
    """
    获取当前模型 主体 id
    :param db:
    :param sub_id:
    :return:
    """
    model = db.query(RegionMarket).filter(
        RegionMarket.sub_id == sub_id
    ).order_by(RegionMarket.id.desc()).first()
    return model.sec_id + 1 if model else 1


def get_paginate_markets(db: Session, page: int = 1, limit: int = 10, sub_id=None, name=None):
    import math
    q = db.query(RegionMarket)
    if name:
        q = q.filter(RegionMarket.name.like("%" + name + "%"))
    count = q.filter(
        RegionMarket.sub_id == sub_id, RegionMarket.deleted_at.is_(None)
    ).count()

    pages = math.ceil(count / limit)
    return get_markets(db=db, page=page, limit=limit, sub_id=sub_id, name=name), count, pages


def get_market_by_sec(db: Session, sec: int, sub_id=None):
    """
    根据主键 获取区域市场
    :param db:
    :param sec:
    :param sub_id:
    :return:
    """
    return db.query(RegionMarket).filter(
        RegionMarket.sub_id == sub_id, RegionMarket.sec_id == sec, RegionMarket.deleted_at.is_(None)
    ).first()


def get_market_by_name(db: Session, name: str, sub_id=None):
    """
    根据名称 获取区域市场
    :param db:
    :param name:
    :param sub_id:
    :return:
    """
    return db.query(RegionMarket).filter(
        RegionMarket.sub_id == sub_id, RegionMarket.name == name, RegionMarket.deleted_at.is_(None)
    ).first()


def create_market(db: Session, market: CreateUpdate):
    """
    创建 区域市场
    :param db:
    :param market:
    :return:
    """
    sec_id = get_model_sec(db=db, sub_id=market.sub_id)
    db_market = RegionMarket(**market.dict(), sec_id=sec_id)
    db.add(db_market)
    db.commit()
    db.refresh(db_market)
    return db_market


def update_market(db: Session, market: CreateUpdate, sec: int, sub_id=None):
    """
    修改 区域市场
    :param db:
    :param market:
    :param sec:
    :param sub_id:
    :return:
    """
    return db.query(RegionMarket).filter(
        RegionMarket.sub_id == sub_id, RegionMarket.sec_id == sec, RegionMarket.deleted_at.is_(None)
    ).update(market.dict(exclude_unset=True)), db.commit(), db.close()


def delete_markets(db: Session, sec: list, sub_id=None):
    """
    删除区域市场 修改删除时间
    :param db:
    :param sec:
    :param sub_id:
    :return:
    """
    from datetime import datetime
    response = db.query(RegionMarket).filter(
        RegionMarket.sub_id == sub_id, RegionMarket.sec_id.in_(sec), RegionMarket.deleted_at.is_(None)
    ).update({"deleted_at": datetime.now()})
    db.commit(), db.close()
    return response
