from sqlalchemy.orm import Session

from .schemas import CreateUpdate
from ..models import MemberSource


def get_sources(db: Session, page: int = 1, limit: int = 10, sub_id=None, name=None):
    """
    获取 添加方式列表
    :param db:
    :param page:
    :param limit:
    :param sub_id:
    :param name:
    :return:
    """
    skip = (page - 1) * limit
    q = db.query(MemberSource)
    if name:
        q = q.filter(MemberSource.name.like("%" + name + "%"))
    return q.filter(
        MemberSource.sub_id == sub_id, MemberSource.deleted_at.is_(None)
    ).offset(skip).limit(limit).all()


def get_model_sec(db: Session, sub_id):
    """
    获取当前模型 主体 id
    :param db:
    :param sub_id:
    :return:
    """
    model = db.query(MemberSource).filter(
        MemberSource.sub_id == sub_id
    ).order_by(MemberSource.id.desc()).first()
    return model.sec_id + 1 if model else 1


def get_paginate_sources(db: Session, page: int = 1, limit: int = 10, sub_id=None, name=None):
    import math
    q = db.query(MemberSource)
    if name:
        q = q.filter(MemberSource.name.like("%" + name + "%"))
    count = q.filter(
        MemberSource.sub_id == sub_id, MemberSource.deleted_at.is_(None)
    ).count()

    pages = math.ceil(count / limit)
    return get_sources(db=db, page=page, limit=limit, sub_id=sub_id, name=name), count, pages


def get_source_by_sec(db: Session, sec: int, sub_id=None):
    """
    根据主键 获取添加方式
    :param db:
    :param sec:
    :param sub_id:
    :return:
    """
    return db.query(MemberSource).filter(
        MemberSource.sub_id == sub_id, MemberSource.sec_id == sec, MemberSource.deleted_at.is_(None)
    ).first()


def get_source_by_name(db: Session, name: str, sub_id=None):
    """
    根据名称 获取添加方式
    :param db:
    :param name:
    :param sub_id:
    :return:
    """
    return db.query(MemberSource).filter(
        MemberSource.sub_id == sub_id, MemberSource.name == name, MemberSource.deleted_at.is_(None)
    ).first()


def create_source(db: Session, source: CreateUpdate):
    """
    创建 添加方式
    :param db:
    :param source:
    :return:
    """
    sec_id = get_model_sec(db=db, sub_id=source.sub_id)
    db_source = MemberSource(**source.dict(), sec_id=sec_id)
    db.add(db_source)
    db.commit()
    db.refresh(db_source)
    return db_source


def update_source(db: Session, source: CreateUpdate, sec: int, sub_id=None):
    """
    修改 添加方式
    :param db:
    :param source:
    :param sec:
    :param sub_id:
    :return:
    """
    return db.query(MemberSource).filter(
        MemberSource.sub_id == sub_id, MemberSource.sec_id == sec, MemberSource.deleted_at.is_(None)
    ).update(source.dict(exclude_unset=True)), db.commit(), db.close()


def delete_sources(db: Session, sec: list, sub_id=None):
    """
    删除添加方式 修改删除时间
    :param db:
    :param sec:
    :param sub_id:
    :return:
    """
    from datetime import datetime
    response = db.query(MemberSource).filter(
        MemberSource.sub_id == sub_id, MemberSource.sec_id.in_(sec), MemberSource.deleted_at.is_(None)
    ).update({"deleted_at": datetime.now()})
    db.commit(), db.close()
    return response
