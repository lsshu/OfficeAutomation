from sqlalchemy.orm import Session

from .schemas import CreateUpdate
from ..models import RegionDivision


def get_divisions(db: Session, page: int = 1, limit: int = 10, sub_id=None, name=None):
    """
    获取 区域事业部列表
    :param db:
    :param page:
    :param limit:
    :param sub_id:
    :param name:
    :return:
    """
    skip = (page - 1) * limit
    q = db.query(RegionDivision)
    if name:
        q = q.filter(RegionDivision.name.like("%" + name + "%"))
    return q.filter(
        RegionDivision.sub_id == sub_id, RegionDivision.deleted_at.is_(None)
    ).offset(skip).limit(limit).all()


def get_model_sec(db: Session, sub_id):
    """
    获取当前模型 主体 id
    :param db:
    :param sub_id:
    :return:
    """
    model = db.query(RegionDivision).filter(
        RegionDivision.sub_id == sub_id
    ).order_by(RegionDivision.id.desc()).first()
    return model.sec_id + 1 if model else 1


def get_paginate_divisions(db: Session, page: int = 1, limit: int = 10, sub_id=None, name=None):
    import math
    q = db.query(RegionDivision)
    if name:
        q = q.filter(RegionDivision.name.like("%" + name + "%"))
    count = q.filter(
        RegionDivision.sub_id == sub_id, RegionDivision.deleted_at.is_(None)
    ).count()

    pages = math.ceil(count / limit)
    return get_divisions(db=db, page=page, limit=limit, sub_id=sub_id, name=name), count, pages


def get_division_by_sec(db: Session, sec: int, sub_id=None):
    """
    根据主键 获取区域事业部
    :param db:
    :param sec:
    :param sub_id:
    :return:
    """
    return db.query(RegionDivision).filter(
        RegionDivision.sub_id == sub_id, RegionDivision.sec_id == sec, RegionDivision.deleted_at.is_(None)
    ).first()


def get_division_by_name(db: Session, name: str, sub_id=None):
    """
    根据名称 获取区域事业部
    :param db:
    :param name:
    :param sub_id:
    :return:
    """
    return db.query(RegionDivision).filter(
        RegionDivision.sub_id == sub_id, RegionDivision.name == name, RegionDivision.deleted_at.is_(None)
    ).first()


def create_division(db: Session, division: CreateUpdate):
    """
    创建 区域事业部
    :param db:
    :param division:
    :return:
    """
    sec_id = get_model_sec(db=db, sub_id=division.sub_id)
    db_division = RegionDivision(**division.dict(), sec_id=sec_id)
    db.add(db_division)
    db.commit()
    db.refresh(db_division)
    return db_division


def update_division(db: Session, division: CreateUpdate, sec: int, sub_id=None):
    """
    修改 区域事业部
    :param db:
    :param division:
    :param sec:
    :param sub_id:
    :return:
    """
    return db.query(RegionDivision).filter(
        RegionDivision.sub_id == sub_id, RegionDivision.sec_id == sec, RegionDivision.deleted_at.is_(None)
    ).update(division.dict(exclude_unset=True)), db.commit(), db.close()


def delete_divisions(db: Session, sec: list, sub_id=None):
    """
    删除区域事业部 修改删除时间
    :param db:
    :param sec:
    :param sub_id:
    :return:
    """
    from datetime import datetime
    response = db.query(RegionDivision).filter(
        RegionDivision.sub_id == sub_id, RegionDivision.sec_id.in_(sec), RegionDivision.deleted_at.is_(None)
    ).update({"deleted_at": datetime.now()})
    db.commit(), db.close()
    return response
