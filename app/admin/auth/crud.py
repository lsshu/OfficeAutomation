from sqlalchemy.orm import Session
from .models import AuthUser


def auth_user_by_username_and_available(db: Session, username: str):
    """
    获取 指定用户名的用户
    :param db:
    :param username:
    :return:
    """
    return db.query(AuthUser).filter(AuthUser.username == username, AuthUser.available == True).first()
