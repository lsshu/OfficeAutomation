from sqlalchemy.orm import Session

from .schemas import MemberAgeGroupCreate, MemberAgeGroupUpdate
from ..models import MemberAgeGroup


def get_ages(db: Session, skip: int = 0, limit: int = 10, sub_id=None):
    """
    获取 年龄段列表
    :param db:
    :param skip:
    :param limit:
    :param sub_id:
    :return:
    """
    if sub_id:
        return db.query(MemberAgeGroup).filter(
            MemberAgeGroup.sub_id == sub_id, MemberAgeGroup.deleted_at.is_(None)
        ).offset(skip).limit(limit).all()
    return db.query(MemberAgeGroup).filter(
        MemberAgeGroup.deleted_at.is_(None)
    ).offset(skip).limit(limit).all()


def get_paginate_ages(db: Session, skip: int = 0, limit: int = 10, sub_id=None):
    import math
    if sub_id:
        count = db.query(MemberAgeGroup).filter(
            MemberAgeGroup.sub_id == sub_id, MemberAgeGroup.deleted_at.is_(None)
        ).count()
    else:
        count = db.query(MemberAgeGroup).filter(
            MemberAgeGroup.deleted_at.is_(None)
        ).count()

    pages = math.ceil(count / limit)
    return {"total": count, "pages": pages, "skip": skip, "limit": limit,
            "data": get_ages(db=db, skip=skip, limit=limit, sub_id=sub_id)}


def get_age_by_pk(db: Session, pk: int, sub_id=None):
    """
    根据主键 获取年龄段
    :param db:
    :param pk:
    :param sub_id:
    :return:
    """
    if sub_id:
        return db.query(MemberAgeGroup).filter(
            MemberAgeGroup.sub_id == sub_id, MemberAgeGroup.id == pk, MemberAgeGroup.deleted_at.is_(None)
        ).first()
    return db.query(MemberAgeGroup).filter(
        MemberAgeGroup.id == pk, MemberAgeGroup.deleted_at.is_(None)
    ).first()


def get_age_by_name(db: Session, name: str, sub_id=None):
    """
    根据名称 获取年龄段
    :param db:
    :param name:
    :param sub_id:
    :return:
    """
    if sub_id:
        return db.query(MemberAgeGroup).filter(
            MemberAgeGroup.sub_id == sub_id, MemberAgeGroup.name == name, MemberAgeGroup.deleted_at.is_(None)
        ).first()
    return db.query(MemberAgeGroup).filter(
        MemberAgeGroup.name == name, MemberAgeGroup.deleted_at.is_(None)
    ).first()


def create_age(db: Session, age: MemberAgeGroupCreate, sub_id=None):
    """
    创建 年龄段
    :param db:
    :param age:
    :param sub_id:
    :return:
    """
    db_age = MemberAgeGroup(**age.dict())
    db.add(db_age)
    db.commit()
    db.refresh(db_age)
    return db_age


def update_age(db: Session, age: MemberAgeGroupUpdate, pk: int, sub_id=None):
    """
    修改 年龄段
    :param db:
    :param age:
    :param pk:
    :param sub_id:
    :return:
    """
    if sub_id:
        db.query(MemberAgeGroup).filter(
            MemberAgeGroup.sub_id == sub_id, MemberAgeGroup.id == pk, MemberAgeGroup.deleted_at.is_(None)
        ).update(age.dict()), db.commit(), db.close()
        return get_age_by_pk(db=db, pk=pk, sub_id=sub_id)
    db.query(MemberAgeGroup).filter(
        MemberAgeGroup.id == pk, MemberAgeGroup.deleted_at.is_(None)
    ).update(age.dict()), db.commit(), db.close()
    return get_age_by_pk(db=db, pk=pk, sub_id=sub_id)


def delete_age(db: Session, pk: int, sub_id=None):
    """
    删除年龄段 修改删除时间
    :param db:
    :param pk:
    :param sub_id:
    :return:
    """
    from datetime import datetime
    if sub_id:
        response = db.query(MemberAgeGroup).filter(
            MemberAgeGroup.sub_id == sub_id, MemberAgeGroup.id == pk, MemberAgeGroup.deleted_at.is_(None)
        ).update({"deleted_at": datetime.now()})
        db.commit(), db.close()
        return response
    response = db.query(MemberAgeGroup).filter(
        MemberAgeGroup.id == pk, MemberAgeGroup.deleted_at.is_(None)
    ).update({"deleted_at": datetime.now()})
    db.commit(), db.close()
    return response
