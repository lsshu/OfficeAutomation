from sqlalchemy.orm import Session

from .schemas import AuthUserCreate, AuthUserUpdate, AuthUserPatch
from ..models import AuthUser


def get_auth_users(db: Session, skip: int = 0, limit: int = 10, sub_id=None):
    """
    获取 授权用户列表
    :param db:
    :param skip:
    :param limit:
    :param sub_id:
    :return:
    """
    if sub_id:
        return db.query(AuthUser).filter(
            AuthUser.sub_id == sub_id, AuthUser.deleted_at.is_(None)
        ).offset(skip).limit(limit).all()
    return db.query(AuthUser).filter(
        AuthUser.deleted_at.is_(None)
    ).offset(skip).limit(limit).all()


def get_model_sec(db: Session, sub_id):
    """
    获取当前模型 主体 id
    :param db:
    :param sub_id:
    :return:
    """
    model = db.query(AuthUser).filter(
        AuthUser.sub_id == sub_id
    ).order_by(AuthUser.id.desc()).first()
    return model.sec_id + 1 if model else 1


def get_paginate_auth_users(db: Session, skip: int = 0, limit: int = 10, sub_id=None):
    import math
    if sub_id:
        count = db.query(AuthUser).filter(
            AuthUser.sub_id == sub_id, AuthUser.deleted_at.is_(None)
        ).count()
    else:
        count = db.query(AuthUser).filter(
            AuthUser.deleted_at.is_(None)
        ).count()

    pages = math.ceil(count / limit)
    return get_auth_users(db=db, skip=skip, limit=limit, sub_id=sub_id), count, pages


def get_auth_user_by_pk(db: Session, pk: int, sub_id=None):
    """
    根据主键 获取授权用户
    :param db:
    :param pk:
    :param sub_id:
    :return:
    """
    if sub_id:
        return db.query(AuthUser).filter(
            AuthUser.sub_id == sub_id, AuthUser.id == pk, AuthUser.deleted_at.is_(None)
        ).first()
    return db.query(AuthUser).filter(
        AuthUser.id == pk, AuthUser.deleted_at.is_(None)
    ).first()


def get_auth_user_by_name(db: Session, name: str, sub_id=None):
    """
    根据名称 获取授权用户
    :param db:
    :param name:
    :param sub_id:
    :return:
    """
    if sub_id:
        return db.query(AuthUser).filter(
            AuthUser.sub_id == sub_id, AuthUser.username == name, AuthUser.deleted_at.is_(None)
        ).first()
    return db.query(AuthUser).filter(
        AuthUser.username == name, AuthUser.deleted_at.is_(None)
    ).first()


def create_auth_user(db: Session, auth_user: AuthUserCreate):
    """
    创建 授权用户
    :param db:
    :param auth_user:
    :return:
    """
    from ..defs import token_get_password_hash
    sec_id = get_model_sec(db=db, sub_id=auth_user.sub_id)
    auth_user.password = token_get_password_hash(auth_user.password)
    db_auth_user = AuthUser(**auth_user.dict(), sec_id=sec_id)
    db.add(db_auth_user)
    db.commit()
    db.refresh(db_auth_user)
    return db_auth_user


def update_auth_user(db: Session, auth_user: AuthUserUpdate, pk: int, sub_id=None):
    """
    修改 授权用户
    :param db:
    :param auth_user:
    :param pk:
    :param sub_id:
    :return:
    """
    from ..defs import token_get_password_hash
    auth_user.password = token_get_password_hash(auth_user.password)

    if sub_id:
        db.query(AuthUser).filter(
            AuthUser.sub_id == sub_id, AuthUser.id == pk, AuthUser.deleted_at.is_(None)
        ).update(auth_user.dict(exclude_unset=True)), db.commit(), db.close()
    else:
        db.query(AuthUser).filter(
            AuthUser.id == pk, AuthUser.deleted_at.is_(None)
        ).update(auth_user.dict(exclude_unset=True)), db.commit(), db.close()
    return get_auth_user_by_pk(db=db, pk=pk, sub_id=sub_id)


def delete_auth_user(db: Session, pk: int, sub_id=None):
    """
    删除授权用户 修改删除时间
    :param db:
    :param pk:
    :param sub_id:
    :return:
    """
    from datetime import datetime
    if sub_id:
        response = db.query(AuthUser).filter(
            AuthUser.sub_id == sub_id, AuthUser.id == pk, AuthUser.deleted_at.is_(None)
        ).update({"deleted_at": datetime.now()})
        db.commit(), db.close()
        return response
    response = db.query(AuthUser).filter(
        AuthUser.id == pk, AuthUser.deleted_at.is_(None)
    ).update({"deleted_at": datetime.now()})
    db.commit(), db.close()
    return response
