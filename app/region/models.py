from datetime import datetime
from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship

try:
    from ..admin.auth.db import Model, Engine
    from ..admin.auth.models import AuthSubject, AuthUser
except:
    from app.admin.auth.db import Model, Engine
    from app.admin.auth.models import AuthSubject, AuthUser


class RegionCompany(Model):
    __tablename__ = "region_companies"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    sub_id = Column(Integer, ForeignKey('auth_subjects.id'), comment='主体pk')
    subject = relationship('AuthSubject', backref='region_companies')
    name = Column(String(15), nullable=False, comment="名称")
    created_at = Column(TIMESTAMP, nullable=True, default=datetime.now, comment="创建日期")
    updated_at = Column(TIMESTAMP, nullable=True, default=datetime.now, onupdate=datetime.now, comment="更新日期")
    deleted_at = Column(TIMESTAMP, nullable=True, comment="删除日期")


class RegionDivision(Model):
    __tablename__ = "region_divisions"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    sub_id = Column(Integer, ForeignKey('auth_subjects.id'), comment='主体pk')
    subject = relationship('AuthSubject', backref='region_divisions')
    name = Column(String(15), nullable=False, comment="名称")
    created_at = Column(TIMESTAMP, nullable=True, default=datetime.now, comment="创建日期")
    updated_at = Column(TIMESTAMP, nullable=True, default=datetime.now, onupdate=datetime.now, comment="更新日期")
    deleted_at = Column(TIMESTAMP, nullable=True, comment="删除日期")


class RegionMarket(Model):
    __tablename__ = "region_markets"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    sub_id = Column(Integer, ForeignKey('auth_subjects.id'), comment='主体pk')
    subject = relationship('AuthSubject', backref='region_markets')
    name = Column(String(15), nullable=False, comment="名称")
    created_at = Column(TIMESTAMP, nullable=True, default=datetime.now, comment="创建日期")
    updated_at = Column(TIMESTAMP, nullable=True, default=datetime.now, onupdate=datetime.now, comment="更新日期")
    deleted_at = Column(TIMESTAMP, nullable=True, comment="删除日期")


if __name__ == '__main__':
    Model.metadata.create_all(Engine)  # 创建表结构
