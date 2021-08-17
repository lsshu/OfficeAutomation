from datetime import datetime

from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship

try:
    from .db import Model, Engine
except:
    from app.admin.auth.db import Model, Engine


class Subject(Model):
    __tablename__ = "subjects"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(10), nullable=False, comment="名称")
    domain = Column(String(25), nullable=False, comment="域名")
    expires_time = Column(TIMESTAMP, nullable=True, comment="到期日期")
    available = Column(Boolean, default=True, comment="是否有效")
    auth_user = relationship('AuthUser', back_populates='subject')  # back_populates来指定反向访问的属性名称
    created_at = Column(TIMESTAMP, nullable=True, default=datetime.now, comment="创建日期")
    updated_at = Column(TIMESTAMP, nullable=True, default=datetime.now, onupdate=datetime.now, comment="更新日期")
    deleted_at = Column(TIMESTAMP, nullable=True, comment="删除日期")


class AuthUser(Model):
    __tablename__ = "auth_users"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    sub_id = Column(Integer, ForeignKey('subjects.id'), comment='所属省/直辖市')
    username = Column(String(15), nullable=False, unique=True, comment="名称")
    password = Column(String(128), nullable=False, comment="密码")
    available = Column(Boolean, default=True, comment="是否有效")
    subject = relationship('Subject', back_populates='auth_user')  # 关联的类名；back_populates来指定反向访问的属性名称
    created_at = Column(TIMESTAMP, nullable=True, default=datetime.now, comment="创建日期")
    updated_at = Column(TIMESTAMP, nullable=True, default=datetime.now, onupdate=datetime.now, comment="更新日期")
    deleted_at = Column(TIMESTAMP, nullable=True, comment="删除日期")


if __name__ == '__main__':
    Model.metadata.create_all(Engine)  # 创建表结构
