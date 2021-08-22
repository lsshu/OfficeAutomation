from sqlalchemy.orm import Session

from .schemas import MemberSourceCreate, MemberSourceUpdate
from ..models import MemberSource


def get_sources(db: Session, skip: int = 0, limit: int = 10, sub_id=None):
    """
    获取 添加方式列表
    :param db:
    :param skip:
    :param limit:
    :param sub_id:
    :return:
    """
    if sub_id:
        return db.query(MemberSource).filter(
            MemberSource.sub_id == sub_id, MemberSource.deleted_at.is_(None)
        ).offset(skip).limit(limit).all()
    return db.query(MemberSource).filter(
        MemberSource.deleted_at.is_(None)
    ).offset(skip).limit(limit).all()


def get_paginate_sources(db: Session, skip: int = 0, limit: int = 10, sub_id=None):
    import math
    if sub_id:
        count = db.query(MemberSource).filter(
            MemberSource.sub_id == sub_id, MemberSource.deleted_at.is_(None)
        ).count()
    else:
        count = db.query(MemberSource).filter(
            MemberSource.deleted_at.is_(None)
        ).count()

    pages = math.ceil(count / limit)
    return {"total": count, "pages": pages, "skip": skip, "limit": limit,
            "data": get_sources(db=db, skip=skip, limit=limit, sub_id=sub_id)}


def get_source_by_pk(db: Session, pk: int, sub_id=None):
    """
    根据主键 获取添加方式
    :param db:
    :param pk:
    :param sub_id:
    :return:
    """
    if sub_id:
        return db.query(MemberSource).filter(
            MemberSource.sub_id == sub_id, MemberSource.id == pk, MemberSource.deleted_at.is_(None)
        ).first()
    return db.query(MemberSource).filter(
        MemberSource.id == pk, MemberSource.deleted_at.is_(None)
    ).first()


def get_source_by_name(db: Session, name: str, sub_id=None):
    """
    根据名称 获取添加方式
    :param db:
    :param name:
    :param sub_id:
    :return:
    """
    if sub_id:
        return db.query(MemberSource).filter(
            MemberSource.sub_id == sub_id, MemberSource.name == name, MemberSource.deleted_at.is_(None)
        ).first()
    return db.query(MemberSource).filter(
        MemberSource.name == name, MemberSource.deleted_at.is_(None)
    ).first()


def create_source(db: Session, source: MemberSourceCreate, sub_id=None):
    """
    创建 添加方式
    :param db:
    :param source:
    :param sub_id:
    :return:
    """
    db_source = MemberSource(**source.dict())
    db.add(db_source)
    db.commit()
    db.refresh(db_source)
    return db_source


def update_source(db: Session, source: MemberSourceUpdate, pk: int, sub_id=None):
    """
    修改 添加方式
    :param db:
    :param source:
    :param pk:
    :param sub_id:
    :return:
    """
    if sub_id:
        db.query(MemberSource).filter(
            MemberSource.sub_id == sub_id, MemberSource.id == pk, MemberSource.deleted_at.is_(None)
        ).update(source.dict()), db.commit(), db.close()
        return get_source_by_pk(db=db, pk=pk, sub_id=sub_id)
    db.query(MemberSource).filter(
        MemberSource.id == pk, MemberSource.deleted_at.is_(None)
    ).update(source.dict()), db.commit(), db.close()
    return get_source_by_pk(db=db, pk=pk, sub_id=sub_id)


def delete_source(db: Session, pk: int, sub_id=None):
    """
    删除添加方式 修改删除时间
    :param db:
    :param pk:
    :param sub_id:
    :return:
    """
    from datetime import datetime
    if sub_id:
        response = db.query(MemberSource).filter(
            MemberSource.sub_id == sub_id, MemberSource.id == pk, MemberSource.deleted_at.is_(None)
        ).update({"deleted_at": datetime.now()})
        db.commit(), db.close()
        return response
    response = db.query(MemberSource).filter(
        MemberSource.id == pk, MemberSource.deleted_at.is_(None)
    ).update({"deleted_at": datetime.now()})
    db.commit(), db.close()
    return response
