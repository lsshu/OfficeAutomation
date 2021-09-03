from sqlalchemy.orm import Session, joinedload
from sqlalchemy.orm.strategy_options import selectinload

from .schemas import MemberUserCreate, MemberUserUpdate
from ..models import MemberUser


def get_users(db: Session, skip: int = 0, limit: int = 10, sub_id=None):
    """
    获取 客户信息列表
    :param db:
    :param skip:
    :param limit:
    :param sub_id:
    :return:
    """
    if sub_id:
        return db.query(MemberUser).options(
            # selectinload(MemberUser.age)
            # joinedload(MemberUser.age)
        ).filter(
            MemberUser.sub_id == sub_id, MemberUser.deleted_at.is_(None)
        ).offset(skip).limit(limit).all()
    return db.query(MemberUser).filter(
        MemberUser.deleted_at.is_(None)
    ).offset(skip).limit(limit).all()


def get_model_sec(db: Session, sub_id):
    """
    获取当前模型 主体 id
    :param db:
    :param sub_id:
    :return:
    """
    model = db.query(MemberUser).filter(
        MemberUser.sub_id == sub_id
    ).order_by(MemberUser.id.desc()).first()
    return model.sec_id + 1 if model else 1


def get_paginate_users(db: Session, page: int = 0, limit: int = 10, sub_id=None):
    import math
    if sub_id:
        count = db.query(MemberUser).filter(
            MemberUser.sub_id == sub_id, MemberUser.deleted_at.is_(None)
        ).count()
    else:
        count = db.query(MemberUser).filter(
            MemberUser.deleted_at.is_(None)
        ).count()

    pages = math.ceil(count / limit)
    skip = (page - 1) * limit
    return get_users(db=db, skip=skip, limit=limit, sub_id=sub_id), count, pages


def get_user_by_pk(db: Session, pk: int, sub_id=None):
    """
    根据主键 获取客户信息
    :param db:
    :param pk:
    :param sub_id:
    :return:
    """
    if sub_id:
        return db.query(MemberUser).options(
            joinedload(MemberUser.age)
        ).filter(
            MemberUser.sub_id == sub_id, MemberUser.id == pk, MemberUser.deleted_at.is_(None)
        ).first()
    return db.query(MemberUser).filter(
        MemberUser.id == pk, MemberUser.deleted_at.is_(None)
    ).first()


def get_user_by_name(db: Session, name: str, sub_id=None):
    """
    根据名称 获取客户信息
    :param db:
    :param name:
    :param sub_id:
    :return:
    """
    if sub_id:
        return db.query(MemberUser).filter(
            MemberUser.sub_id == sub_id, MemberUser.username == name, MemberUser.deleted_at.is_(None)
        ).first()
    return db.query(MemberUser).filter(
        MemberUser.username == name, MemberUser.deleted_at.is_(None)
    ).first()


def create_user(db: Session, user: MemberUserCreate, auth, sub_id=None):
    """
    创建 客户信息
    :param db:
    :param user:
    :param auth:
    :param sub_id:
    :return:
    """
    sec_id = get_model_sec(db=db, sub_id=user.sub_id)
    db_user = MemberUser(**user.dict(), sec_id=sec_id, own_id=auth.user_id)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user: MemberUserUpdate, pk: int, sub_id=None):
    """
    修改 客户信息
    :param db:
    :param user:
    :param pk:
    :param sub_id:
    :return:
    """
    if sub_id:
        db.query(MemberUser).filter(
            MemberUser.sub_id == sub_id, MemberUser.id == pk, MemberUser.deleted_at.is_(None)
        ).update(user.dict()), db.commit(), db.close()
        return get_user_by_pk(db=db, pk=pk, sub_id=sub_id)
    db.query(MemberUser).filter(
        MemberUser.id == pk, MemberUser.deleted_at.is_(None)
    ).update(user.dict()), db.commit(), db.close()
    return get_user_by_pk(db=db, pk=pk, sub_id=sub_id)


def delete_user(db: Session, pk: int, sub_id=None):
    """
    删除客户信息 修改删除时间
    :param db:
    :param pk:
    :param sub_id:
    :return:
    """
    from datetime import datetime
    if sub_id:
        response = db.query(MemberUser).filter(
            MemberUser.sub_id == sub_id, MemberUser.id == pk, MemberUser.deleted_at.is_(None)
        ).update({"deleted_at": datetime.now()})
        db.commit(), db.close()
        return response
    response = db.query(MemberUser).filter(
        MemberUser.id == pk, MemberUser.deleted_at.is_(None)
    ).update({"deleted_at": datetime.now()})
    db.commit(), db.close()
    return response
