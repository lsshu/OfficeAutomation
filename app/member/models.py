from datetime import datetime

from sqlalchemy import Column, Integer, String, CHAR, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship

try:
    from ..admin.auth.db import Model, Engine
    from ..region.models import RegionCompany, RegionDivision, RegionMarket, AuthSubject, AuthUser
except:
    from app.admin.auth.db import Model, Engine
    from app.region.models import RegionCompany, RegionDivision, RegionMarket, AuthSubject, AuthUser


class MemberAgeGroup(Model):
    """年龄段"""
    __tablename__ = "member_age_groups"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    sec_id = Column(Integer, index=True, comment='次要id')
    sub_id = Column(Integer, ForeignKey('auth_subjects.id'), comment='主体')
    subject = relationship('AuthSubject', backref='member_age_groups')
    name = Column(String(15), nullable=True, comment="名称")
    created_at = Column(TIMESTAMP, nullable=True, default=datetime.now, comment="创建日期")
    updated_at = Column(TIMESTAMP, nullable=True, default=datetime.now, onupdate=datetime.now, comment="更新日期")
    deleted_at = Column(TIMESTAMP, nullable=True, comment="删除日期")


class MemberSource(Model):
    """添加方式"""
    __tablename__ = "member_sources"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    sec_id = Column(Integer, index=True, comment='次要id')
    sub_id = Column(Integer, ForeignKey('auth_subjects.id'), comment='主体')
    subject = relationship('AuthSubject', backref='member_sources')
    name = Column(String(15), nullable=True, comment="名称")
    created_at = Column(TIMESTAMP, nullable=True, default=datetime.now, comment="创建日期")
    updated_at = Column(TIMESTAMP, nullable=True, default=datetime.now, onupdate=datetime.now, comment="更新日期")
    deleted_at = Column(TIMESTAMP, nullable=True, comment="删除日期")


class MemberQualityType(Model):
    """粉质量类别"""
    __tablename__ = "member_quality_types"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    sec_id = Column(Integer, index=True, comment='次要id')
    sub_id = Column(Integer, ForeignKey('auth_subjects.id'), comment='主体')
    subject = relationship('AuthSubject', backref='member_quality_types')
    name = Column(String(15), nullable=True, comment="名称")
    created_at = Column(TIMESTAMP, nullable=True, default=datetime.now, comment="创建日期")
    updated_at = Column(TIMESTAMP, nullable=True, default=datetime.now, onupdate=datetime.now, comment="更新日期")
    deleted_at = Column(TIMESTAMP, nullable=True, comment="删除日期")


class MemberUser(Model):
    """客户信息"""
    __tablename__ = "member_users"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    sec_id = Column(Integer, index=True, comment='次要id')
    sub_id = Column(Integer, ForeignKey('auth_subjects.id'), comment='主体')
    subject = relationship('AuthSubject', backref='member_users')
    com_id = Column(Integer, ForeignKey('region_companies.id'), comment='公司')
    company = relationship('RegionCompany', backref='member_users')
    div_id = Column(Integer, ForeignKey('region_divisions.id'), comment='事业部')
    division = relationship('RegionDivision', backref='member_users')
    mar_id = Column(Integer, ForeignKey('region_markets.id'), comment='市场')
    market = relationship('RegionMarket', backref='member_users')
    own_id = Column(Integer, ForeignKey('auth_users.id'), comment='账号')
    owner = relationship('AuthUser', backref='member_users')

    age_id = Column(Integer, ForeignKey('member_age_groups.id'), comment='年龄段')
    age = relationship('MemberAgeGroup', backref='member_users')
    sou_id = Column(Integer, ForeignKey('member_sources.id'), comment='添加方式')
    source = relationship('MemberSource', backref='member_users')
    qua_id = Column(Integer, ForeignKey('member_quality_types.id'), comment='粉质量类别')
    quality = relationship('MemberQualityType', backref='member_users')

    own_wx = Column(String(15), nullable=True, comment="所属微信")
    username = Column(String(15), nullable=True, comment="客户")
    telephone = Column(String(11), nullable=True, comment="电话")
    wx_number = Column(String(30), nullable=True, comment="微信号")
    wx_nickname = Column(String(20), nullable=True, comment="微信昵称")
    gender = Column(String(1), nullable=True, comment="性别")
    asc_province = Column(Integer, nullable=True, comment='所在省')
    asc_city = Column(Integer, nullable=True, comment='所在市')
    pass_at = Column(TIMESTAMP, nullable=True, comment="加粉日期")
    tra_status = Column(CHAR(1), nullable=True, comment='客户状态')

    created_at = Column(TIMESTAMP, nullable=True, default=datetime.now, comment="创建日期")
    updated_at = Column(TIMESTAMP, nullable=True, default=datetime.now, onupdate=datetime.now, comment="更新日期")
    deleted_at = Column(TIMESTAMP, nullable=True, comment="删除日期")


if __name__ == '__main__':
    Model.metadata.create_all(Engine)  # 创建表结构
