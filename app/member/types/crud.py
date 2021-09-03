from sqlalchemy.orm import Session

from .schemas import CreateUpdate
from ..models import MemberType


def get_types(db: Session, page: int = 1, limit: int = 10, sub_id=None, name=None):
    """
    获取 加粉类别列表
    :param db:
    :param page:
    :param limit:
    :param sub_id:
    :param name:
    :return:
    """
    skip = (page - 1) * limit
    q = db.query(MemberType)
    if name:
        q = q.filter(MemberType.name.like("%" + name + "%"))
    return q.filter(
        MemberType.sub_id == sub_id, MemberType.deleted_at.is_(None)
    ).offset(skip).limit(limit).all()


def get_model_sec(db: Session, sub_id):
    """
    获取当前模型 主体 id
    :param db:
    :param sub_id:
    :return:
    """
    model = db.query(MemberType).filter(
        MemberType.sub_id == sub_id
    ).order_by(MemberType.id.desc()).first()
    return model.sec_id + 1 if model else 1


def get_paginate_types(db: Session, page: int = 1, limit: int = 10, sub_id=None, name=None):
    import math
    q = db.query(MemberType)
    if name:
        q = q.filter(MemberType.name.like("%" + name + "%"))
    count = q.filter(
        MemberType.sub_id == sub_id, MemberType.deleted_at.is_(None)
    ).count()

    pages = math.ceil(count / limit)
    return get_types(db=db, page=page, limit=limit, sub_id=sub_id, name=name), count, pages


def get_type_by_sec(db: Session, sec: int, sub_id=None):
    """
    根据主键 获取加粉类别
    :param db:
    :param sec:
    :param sub_id:
    :return:
    """
    return db.query(MemberType).filter(
        MemberType.sub_id == sub_id, MemberType.sec_id == sec, MemberType.deleted_at.is_(None)
    ).first()


def get_type_by_name(db: Session, name: str, sub_id=None):
    """
    根据名称 获取加粉类别
    :param db:
    :param name:
    :param sub_id:
    :return:
    """
    return db.query(MemberType).filter(
        MemberType.sub_id == sub_id, MemberType.name == name, MemberType.deleted_at.is_(None)
    ).first()


def create_type(db: Session, type: CreateUpdate):
    """
    创建 加粉类别
    :param db:
    :param type:
    :return:
    """
    sec_id = get_model_sec(db=db, sub_id=type.sub_id)
    db_type = MemberType(**type.dict(), sec_id=sec_id)
    db.add(db_type)
    db.commit()
    db.refresh(db_type)
    return db_type


def update_type(db: Session, type: CreateUpdate, sec: int, sub_id=None):
    """
    修改 加粉类别
    :param db:
    :param type:
    :param sec:
    :param sub_id:
    :return:
    """
    return db.query(MemberType).filter(
        MemberType.sub_id == sub_id, MemberType.sec_id == sec, MemberType.deleted_at.is_(None)
    ).update(type.dict(exclude_unset=True)), db.commit(), db.close()


def delete_types(db: Session, sec: list, sub_id=None):
    """
    删除加粉类别 修改删除时间
    :param db:
    :param sec:
    :param sub_id:
    :return:
    """
    from datetime import datetime
    response = db.query(MemberType).filter(
        MemberType.sub_id == sub_id, MemberType.sec_id.in_(sec), MemberType.deleted_at.is_(None)
    ).update({"deleted_at": datetime.now()})
    db.commit(), db.close()
    return response
