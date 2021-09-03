from sqlalchemy.orm import Session

from .schemas import CreateUpdate
from ..models import MemberAgeGroup


def get_ages(db: Session, page: int = 1, limit: int = 10, sub_id=None, name=None):
    """
    获取 年龄段列表
    :param db:
    :param page:
    :param limit:
    :param sub_id:
    :param name:
    :return:
    """
    skip = (page - 1) * limit
    q = db.query(MemberAgeGroup)
    if name:
        q = q.filter(MemberAgeGroup.name.like("%" + name + "%"))
    return q.filter(
        MemberAgeGroup.sub_id == sub_id, MemberAgeGroup.deleted_at.is_(None)
    ).offset(skip).limit(limit).all()


def get_model_sec(db: Session, sub_id):
    """
    获取当前模型 主体 id
    :param db:
    :param sub_id:
    :return:
    """
    model = db.query(MemberAgeGroup).filter(
        MemberAgeGroup.sub_id == sub_id
    ).order_by(MemberAgeGroup.id.desc()).first()
    return model.sec_id + 1 if model else 1


def get_paginate_ages(db: Session, page: int = 1, limit: int = 10, sub_id=None, name=None):
    import math
    q = db.query(MemberAgeGroup)
    if name:
        q = q.filter(MemberAgeGroup.name.like("%" + name + "%"))
    count = q.filter(
        MemberAgeGroup.sub_id == sub_id, MemberAgeGroup.deleted_at.is_(None)
    ).count()

    pages = math.ceil(count / limit)
    return get_ages(db=db, page=page, limit=limit, sub_id=sub_id, name=name), count, pages


def get_age_by_sec(db: Session, sec: int, sub_id=None):
    """
    根据主键 获取年龄段
    :param db:
    :param sec:
    :param sub_id:
    :return:
    """
    return db.query(MemberAgeGroup).filter(
        MemberAgeGroup.sub_id == sub_id, MemberAgeGroup.sec_id == sec, MemberAgeGroup.deleted_at.is_(None)
    ).first()


def get_age_by_name(db: Session, name: str, sub_id=None):
    """
    根据名称 获取年龄段
    :param db:
    :param name:
    :param sub_id:
    :return:
    """
    return db.query(MemberAgeGroup).filter(
        MemberAgeGroup.sub_id == sub_id, MemberAgeGroup.name == name, MemberAgeGroup.deleted_at.is_(None)
    ).first()


def create_age(db: Session, age: CreateUpdate):
    """
    创建 年龄段
    :param db:
    :param age:
    :return:
    """
    sec_id = get_model_sec(db=db, sub_id=age.sub_id)
    db_age = MemberAgeGroup(**age.dict(), sec_id=sec_id)
    db.add(db_age)
    db.commit()
    db.refresh(db_age)
    return db_age


def update_age(db: Session, age: CreateUpdate, sec: int, sub_id=None):
    """
    修改 年龄段
    :param db:
    :param age:
    :param sec:
    :param sub_id:
    :return:
    """
    return db.query(MemberAgeGroup).filter(
        MemberAgeGroup.sub_id == sub_id, MemberAgeGroup.sec_id == sec, MemberAgeGroup.deleted_at.is_(None)
    ).update(age.dict(exclude_unset=True)), db.commit(), db.close()


def delete_ages(db: Session, sec: list, sub_id=None):
    """
    删除年龄段 修改删除时间
    :param db:
    :param sec:
    :param sub_id:
    :return:
    """
    from datetime import datetime
    response = db.query(MemberAgeGroup).filter(
        MemberAgeGroup.sub_id == sub_id, MemberAgeGroup.sec_id.in_(sec), MemberAgeGroup.deleted_at.is_(None)
    ).update({"deleted_at": datetime.now()})
    db.commit(), db.close()
    return response
