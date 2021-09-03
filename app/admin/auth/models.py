from datetime import datetime

from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, ForeignKey, Table
from sqlalchemy.orm import relationship

try:
    from .db import Model, Engine
except:
    from app.admin.auth.db import Model, Engine


class AuthSubject(Model):
    """主体"""
    __tablename__ = "auth_subjects"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(15), nullable=False, comment="名称")
    domain = Column(String(25), nullable=False, comment="域名")
    expires_time = Column(TIMESTAMP, nullable=True, comment="到期日期")
    available = Column(Boolean, default=True, comment="是否有效")
    # auth_users = relationship('AuthUser', back_populates='subject')  # back_populates来指定反向访问的属性名称
    created_at = Column(TIMESTAMP, nullable=True, default=datetime.now, comment="创建日期")
    updated_at = Column(TIMESTAMP, nullable=True, default=datetime.now, onupdate=datetime.now, comment="更新日期")
    deleted_at = Column(TIMESTAMP, nullable=True, comment="删除日期")


class AuthUser(Model):
    """登录用户"""
    __tablename__ = "auth_users"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    sec_id = Column(Integer, index=True, comment='次要id')
    sub_id = Column(Integer, ForeignKey('auth_subjects.id'), comment='主体pk')
    subject = relationship('AuthSubject', backref='auth_users')  # 关联的类名；back_populates来指定反向访问的属性名称
    # subject = relationship('AuthSubject', back_populates='auth_users')  # 关联的类名；back_populates来指定反向访问的属性名称

    username = Column(String(15), nullable=False, unique=True, index=True, comment="名称")
    password = Column(String(128), nullable=False, comment="密码")
    available = Column(Boolean, default=1, comment="是否有效")
    permissions = relationship('AuthPermissions', backref='auth_users', secondary=Table(
        'auth_user_has_permissions',  # 第三张表名
        Model.metadata,  # 元类的数据
        Column('permission_id', Integer, ForeignKey('auth_permissions.id'), primary_key=True, comment="权限"),  # 权限
        Column('user_id', Integer, ForeignKey('auth_users.id'), primary_key=True, comment="用户"),
    ))
    roles = relationship('AuthRoles', backref='auth_users', secondary=Table(
        'auth_user_has_roles',  # 第三张表名
        Model.metadata,  # 元类的数据
        Column('role_id', Integer, ForeignKey('auth_roles.id'), primary_key=True, comment="角色"),  # 角色
        Column('user_id', Integer, ForeignKey('auth_users.id'), primary_key=True, comment="用户"),
    ))
    created_at = Column(TIMESTAMP, nullable=True, default=datetime.now, comment="创建日期")
    updated_at = Column(TIMESTAMP, nullable=True, default=datetime.now, onupdate=datetime.now, comment="更新日期")
    deleted_at = Column(TIMESTAMP, nullable=True, comment="删除日期")


class AuthRoles(Model):
    """角色"""
    __tablename__ = "auth_roles"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    sec_id = Column(Integer, index=True, comment='次要id')
    sub_id = Column(Integer, ForeignKey('auth_subjects.id'), comment='主体pk')
    subject = relationship('AuthSubject', backref='auth_roles')
    name = Column(String(15), nullable=False, unique=True, comment="名称")
    permissions = relationship('AuthPermissions', backref='roles', secondary=Table(
        'auth_role_has_permissions',  # 第三张表名
        Model.metadata,  # 元类的数据
        Column('permission_id', Integer, ForeignKey('auth_permissions.id'), primary_key=True, comment="权限"),  # 权限
        Column('role_id', Integer, ForeignKey('auth_roles.id'), primary_key=True, comment="角色"),  # 角色
        # 两字段primary_key都等于True，组合主键唯一，防止内容一样
    ))
    created_at = Column(TIMESTAMP, nullable=True, default=datetime.now, comment="创建日期")
    updated_at = Column(TIMESTAMP, nullable=True, default=datetime.now, onupdate=datetime.now, comment="更新日期")
    deleted_at = Column(TIMESTAMP, nullable=True, comment="删除日期")


class AuthPermissions(Model):
    """ 权限 """
    __tablename__ = "auth_permissions"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    sec_id = Column(Integer, index=True, comment='次要id')
    sub_id = Column(Integer, ForeignKey('auth_subjects.id'), comment='主体pk')
    subject = relationship('AuthSubject', backref='auth_permissions')
    name = Column(String(15), nullable=False, unique=True, comment="名称")
    created_at = Column(TIMESTAMP, nullable=True, default=datetime.now, comment="创建日期")
    updated_at = Column(TIMESTAMP, nullable=True, default=datetime.now, onupdate=datetime.now, comment="更新日期")
    deleted_at = Column(TIMESTAMP, nullable=True, comment="删除日期")


if __name__ == '__main__':
    Model.metadata.create_all(Engine)  # 创建表结构
