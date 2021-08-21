from sqlalchemy.orm import Session
from .models import AuthUser, AuthSubject


def auth_user_by_username_and_available(db: Session, username: str):
    """
    获取 指定用户名的用户
    :param db:
    :param username:
    :return:
    """
    return db.query(AuthUser).filter(AuthUser.username == username, AuthUser.available == True).first()


def auth_user_by_pk(db: Session, pk: int):
    """
    根据主键 获取授权用户
    :param db:
    :param pk:
    :return:
    """
    return db.query(AuthUser).filter(AuthUser.id == pk).first()


def subjects_by_pk(db: Session, pk: int):
    """
    根据主键 获取主体
    :param db:
    :param pk:
    :return:
    """
    return db.query(AuthSubject).filter(AuthSubject.id == pk).first()


def get_subjects(db: Session, skip: int = 0, limit: int = 10):
    """
    获取 主体信息列表
    :param db:
    :param skip:
    :param limit:
    :return:
    """
    return db.query(AuthSubject).offset(skip).limit(limit).all()


def get_subject_by_pk(db: Session, pk: int):
    """
    根据主键 获取主体
    :param db:
    :param pk:
    :return:
    """
    return db.query(AuthSubject).filter(AuthSubject.id == pk).first()
