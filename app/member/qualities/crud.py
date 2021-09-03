from sqlalchemy.orm import Session

from .schemas import CreateUpdate
from ..models import MemberQualityType


def get_quality_types(db: Session, page: int = 1, limit: int = 10, sub_id=None, name=None):
    """
    获取 加粉质量列表
    :param db:
    :param page:
    :param limit:
    :param sub_id:
    :param name:
    :return:
    """
    skip = (page - 1) * limit
    q = db.query(MemberQualityType)
    if name:
        q = q.filter(MemberQualityType.name.like("%" + name + "%"))
    return q.filter(
        MemberQualityType.sub_id == sub_id, MemberQualityType.deleted_at.is_(None)
    ).offset(skip).limit(limit).all()


def get_model_sec(db: Session, sub_id):
    """
    获取当前模型 主体 id
    :param db:
    :param sub_id:
    :return:
    """
    model = db.query(MemberQualityType).filter(
        MemberQualityType.sub_id == sub_id
    ).order_by(MemberQualityType.id.desc()).first()
    return model.sec_id + 1 if model else 1


def get_paginate_quality_types(db: Session, page: int = 1, limit: int = 10, sub_id=None, name=None):
    import math
    q = db.query(MemberQualityType)
    if name:
        q = q.filter(MemberQualityType.name.like("%" + name + "%"))
    count = q.filter(
        MemberQualityType.sub_id == sub_id, MemberQualityType.deleted_at.is_(None)
    ).count()

    pages = math.ceil(count / limit)
    return get_quality_types(db=db, page=page, limit=limit, sub_id=sub_id, name=name), count, pages


def get_quality_type_by_sec(db: Session, sec: int, sub_id=None):
    """
    根据主键 获取加粉质量
    :param db:
    :param sec:
    :param sub_id:
    :return:
    """
    return db.query(MemberQualityType).filter(
        MemberQualityType.sub_id == sub_id, MemberQualityType.sec_id == sec, MemberQualityType.deleted_at.is_(None)
    ).first()


def get_quality_type_by_name(db: Session, name: str, sub_id=None):
    """
    根据名称 获取加粉质量
    :param db:
    :param name:
    :param sub_id:
    :return:
    """
    return db.query(MemberQualityType).filter(
        MemberQualityType.sub_id == sub_id, MemberQualityType.name == name, MemberQualityType.deleted_at.is_(None)
    ).first()


def create_quality_type(db: Session, quality_type: CreateUpdate):
    """
    创建 加粉质量
    :param db:
    :param quality_type:
    :return:
    """
    sec_id = get_model_sec(db=db, sub_id=quality_type.sub_id)
    db_quality_type = MemberQualityType(**quality_type.dict(), sec_id=sec_id)
    db.add(db_quality_type)
    db.commit()
    db.refresh(db_quality_type)
    return db_quality_type


def update_quality_type(db: Session, quality_type: CreateUpdate, sec: int, sub_id=None):
    """
    修改 加粉质量
    :param db:
    :param quality_type:
    :param sec:
    :param sub_id:
    :return:
    """
    return db.query(MemberQualityType).filter(
        MemberQualityType.sub_id == sub_id, MemberQualityType.sec_id == sec, MemberQualityType.deleted_at.is_(None)
    ).update(quality_type.dict(exclude_unset=True)), db.commit(), db.close()


def delete_quality_types(db: Session, sec: list, sub_id=None):
    """
    删除加粉质量 修改删除时间
    :param db:
    :param sec:
    :param sub_id:
    :return:
    """
    from datetime import datetime
    response = db.query(MemberQualityType).filter(
        MemberQualityType.sub_id == sub_id, MemberQualityType.sec_id.in_(sec), MemberQualityType.deleted_at.is_(None)
    ).update({"deleted_at": datetime.now()})
    db.commit(), db.close()
    return response
