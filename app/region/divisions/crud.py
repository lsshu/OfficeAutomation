from sqlalchemy.orm import Session

from .schemas import RegionDivisionCreate, RegionDivisionUpdate
from ..models import RegionDivision


def get_divisions(db: Session, skip: int = 0, limit: int = 10, sub_id=None):
    """
    获取 区域事业部列表
    :param db:
    :param skip:
    :param limit:
    :param sub_id:
    :return:
    """
    if sub_id:
        return db.query(RegionDivision).filter(
            RegionDivision.sub_id == sub_id, RegionDivision.deleted_at.is_(None)
        ).offset(skip).limit(limit).all()
    return db.query(RegionDivision).filter(
        RegionDivision.deleted_at.is_(None)
    ).offset(skip).limit(limit).all()


def get_paginate_divisions(db: Session, skip: int = 0, limit: int = 10, sub_id=None):
    import math
    if sub_id:
        count = db.query(RegionDivision).filter(
            RegionDivision.sub_id == sub_id, RegionDivision.deleted_at.is_(None)
        ).count()
    else:
        count = db.query(RegionDivision).filter(
            RegionDivision.deleted_at.is_(None)
        ).count()

    pages = math.ceil(count / limit)
    return {"total": count, "pages": pages, "skip": skip, "limit": limit,
            "data": get_divisions(db=db, skip=skip, limit=limit, sub_id=sub_id)}


def get_division_by_pk(db: Session, pk: int, sub_id=None):
    """
    根据主键 获取区域事业部
    :param db:
    :param pk:
    :param sub_id:
    :return:
    """
    if sub_id:
        return db.query(RegionDivision).filter(
            RegionDivision.sub_id == sub_id, RegionDivision.id == pk, RegionDivision.deleted_at.is_(None)
        ).first()
    return db.query(RegionDivision).filter(
        RegionDivision.id == pk, RegionDivision.deleted_at.is_(None)
    ).first()


def get_division_by_name(db: Session, name: str, sub_id=None):
    """
    根据名称 获取区域事业部
    :param db:
    :param name:
    :param sub_id:
    :return:
    """
    if sub_id:
        return db.query(RegionDivision).filter(
            RegionDivision.sub_id == sub_id, RegionDivision.name == name, RegionDivision.deleted_at.is_(None)
        ).first()
    return db.query(RegionDivision).filter(
        RegionDivision.name == name, RegionDivision.deleted_at.is_(None)
    ).first()


def create_division(db: Session, division: RegionDivisionCreate, sub_id=None):
    """
    创建 区域事业部
    :param db:
    :param division:
    :param sub_id:
    :return:
    """
    db_division = RegionDivision(**division.dict())
    db.add(db_division)
    db.commit()
    db.refresh(db_division)
    return db_division


def update_division(db: Session, division: RegionDivisionUpdate, pk: int, sub_id=None):
    """
    修改 区域事业部
    :param db:
    :param division:
    :param pk:
    :param sub_id:
    :return:
    """
    if sub_id:
        db.query(RegionDivision).filter(
            RegionDivision.sub_id == sub_id, RegionDivision.id == pk, RegionDivision.deleted_at.is_(None)
        ).update(division.dict()), db.commit(), db.close()
        return get_division_by_pk(db=db, pk=pk, sub_id=sub_id)
    db.query(RegionDivision).filter(
        RegionDivision.id == pk, RegionDivision.deleted_at.is_(None)
    ).update(division.dict()), db.commit(), db.close()
    return get_division_by_pk(db=db, pk=pk, sub_id=sub_id)


def delete_division(db: Session, pk: int, sub_id=None):
    """
    删除区域事业部 修改删除时间
    :param db:
    :param pk:
    :param sub_id:
    :return:
    """
    from datetime import datetime
    if sub_id:
        response = db.query(RegionDivision).filter(
            RegionDivision.sub_id == sub_id, RegionDivision.id == pk, RegionDivision.deleted_at.is_(None)
        ).update({"deleted_at": datetime.now()})
        db.commit(), db.close()
        return response
    response = db.query(RegionDivision).filter(
        RegionDivision.id == pk, RegionDivision.deleted_at.is_(None)
    ).update({"deleted_at": datetime.now()})
    db.commit(), db.close()
    return response
