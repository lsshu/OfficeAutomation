from sqlalchemy.orm import Session

from .schemas import MemberQualityTypeCreate, MemberQualityTypeUpdate
from ..models import MemberQualityType


def get_quality_types(db: Session, skip: int = 0, limit: int = 10, sub_id=None):
    """
    获取 粉质量类别列表
    :param db:
    :param skip:
    :param limit:
    :param sub_id:
    :return:
    """
    if sub_id:
        return db.query(MemberQualityType).filter(
            MemberQualityType.sub_id == sub_id, MemberQualityType.deleted_at.is_(None)
        ).offset(skip).limit(limit).all()
    return db.query(MemberQualityType).filter(
        MemberQualityType.deleted_at.is_(None)
    ).offset(skip).limit(limit).all()


def get_paginate_quality_types(db: Session, skip: int = 0, limit: int = 10, sub_id=None):
    import math
    if sub_id:
        count = db.query(MemberQualityType).filter(
            MemberQualityType.sub_id == sub_id, MemberQualityType.deleted_at.is_(None)
        ).count()
    else:
        count = db.query(MemberQualityType).filter(
            MemberQualityType.deleted_at.is_(None)
        ).count()

    pages = math.ceil(count / limit)
    return {"total": count, "pages": pages, "skip": skip, "limit": limit,
            "data": get_quality_types(db=db, skip=skip, limit=limit, sub_id=sub_id)}


def get_quality_type_by_pk(db: Session, pk: int, sub_id=None):
    """
    根据主键 获取粉质量类别
    :param db:
    :param pk:
    :param sub_id:
    :return:
    """
    if sub_id:
        return db.query(MemberQualityType).filter(
            MemberQualityType.sub_id == sub_id, MemberQualityType.id == pk, MemberQualityType.deleted_at.is_(None)
        ).first()
    return db.query(MemberQualityType).filter(
        MemberQualityType.id == pk, MemberQualityType.deleted_at.is_(None)
    ).first()


def get_quality_type_by_name(db: Session, name: str, sub_id=None):
    """
    根据名称 获取粉质量类别
    :param db:
    :param name:
    :param sub_id:
    :return:
    """
    if sub_id:
        return db.query(MemberQualityType).filter(
            MemberQualityType.sub_id == sub_id, MemberQualityType.name == name, MemberQualityType.deleted_at.is_(None)
        ).first()
    return db.query(MemberQualityType).filter(
        MemberQualityType.name == name, MemberQualityType.deleted_at.is_(None)
    ).first()


def create_quality_type(db: Session, quality_type: MemberQualityTypeCreate, sub_id=None):
    """
    创建 粉质量类别
    :param db:
    :param quality_type:
    :param sub_id:
    :return:
    """
    db_quality_type = MemberQualityType(**quality_type.dict())
    db.add(db_quality_type)
    db.commit()
    db.refresh(db_quality_type)
    return db_quality_type


def update_quality_type(db: Session, quality_type: MemberQualityTypeUpdate, pk: int, sub_id=None):
    """
    修改 粉质量类别
    :param db:
    :param quality_type:
    :param pk:
    :param sub_id:
    :return:
    """
    if sub_id:
        db.query(MemberQualityType).filter(
            MemberQualityType.sub_id == sub_id, MemberQualityType.id == pk, MemberQualityType.deleted_at.is_(None)
        ).update(quality_type.dict()), db.commit(), db.close()
        return get_quality_type_by_pk(db=db, pk=pk, sub_id=sub_id)
    db.query(MemberQualityType).filter(
        MemberQualityType.id == pk, MemberQualityType.deleted_at.is_(None)
    ).update(quality_type.dict()), db.commit(), db.close()
    return get_quality_type_by_pk(db=db, pk=pk, sub_id=sub_id)


def delete_quality_type(db: Session, pk: int, sub_id=None):
    """
    删除粉质量类别 修改删除时间
    :param db:
    :param pk:
    :param sub_id:
    :return:
    """
    from datetime import datetime
    if sub_id:
        response = db.query(MemberQualityType).filter(
            MemberQualityType.sub_id == sub_id, MemberQualityType.id == pk, MemberQualityType.deleted_at.is_(None)
        ).update({"deleted_at": datetime.now()})
        db.commit(), db.close()
        return response
    response = db.query(MemberQualityType).filter(
        MemberQualityType.id == pk, MemberQualityType.deleted_at.is_(None)
    ).update({"deleted_at": datetime.now()})
    db.commit(), db.close()
    return response
