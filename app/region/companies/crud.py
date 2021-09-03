from sqlalchemy.orm import Session

from .schemas import CreateUpdate
from ..models import RegionCompany


def get_companies(db: Session, page: int = 1, limit: int = 10, sub_id=None, name=None):
    """
    获取 区域公司列表
    :param db:
    :param page:
    :param limit:
    :param sub_id:
    :param name:
    :return:
    """
    skip = (page - 1) * limit
    q = db.query(RegionCompany)
    if name:
        q = q.filter(RegionCompany.name.like("%" + name + "%"))
    return q.filter(
        RegionCompany.sub_id == sub_id, RegionCompany.deleted_at.is_(None)
    ).offset(skip).limit(limit).all()


def get_model_sec(db: Session, sub_id):
    """
    获取当前模型 主体 id
    :param db:
    :param sub_id:
    :return:
    """
    model = db.query(RegionCompany).filter(
        RegionCompany.sub_id == sub_id
    ).order_by(RegionCompany.id.desc()).first()
    return model.sec_id + 1 if model else 1


def get_paginate_companies(db: Session, page: int = 1, limit: int = 10, sub_id=None, name=None):
    import math
    q = db.query(RegionCompany)
    if name:
        q = q.filter(RegionCompany.name.like("%" + name + "%"))
    count = q.filter(
        RegionCompany.sub_id == sub_id, RegionCompany.deleted_at.is_(None)
    ).count()

    pages = math.ceil(count / limit)
    return get_companies(db=db, page=page, limit=limit, sub_id=sub_id, name=name), count, pages


def get_company_by_sec(db: Session, sec: int, sub_id=None):
    """
    根据主键 获取区域公司
    :param db:
    :param sec:
    :param sub_id:
    :return:
    """
    return db.query(RegionCompany).filter(
        RegionCompany.sub_id == sub_id, RegionCompany.sec_id == sec, RegionCompany.deleted_at.is_(None)
    ).first()


def get_company_by_name(db: Session, name: str, sub_id=None):
    """
    根据名称 获取区域公司
    :param db:
    :param name:
    :param sub_id:
    :return:
    """
    return db.query(RegionCompany).filter(
        RegionCompany.sub_id == sub_id, RegionCompany.name == name, RegionCompany.deleted_at.is_(None)
    ).first()


def create_company(db: Session, company: CreateUpdate):
    """
    创建 区域公司
    :param db:
    :param company:
    :return:
    """
    sec_id = get_model_sec(db=db, sub_id=company.sub_id)
    db_company = RegionCompany(**company.dict(), sec_id=sec_id)
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company


def update_company(db: Session, company: CreateUpdate, sec: int, sub_id=None):
    """
    修改 区域公司
    :param db:
    :param company:
    :param sec:
    :param sub_id:
    :return:
    """
    return db.query(RegionCompany).filter(
        RegionCompany.sub_id == sub_id, RegionCompany.sec_id == sec, RegionCompany.deleted_at.is_(None)
    ).update(company.dict(exclude_unset=True)), db.commit(), db.close()


def delete_companies(db: Session, sec: list, sub_id=None):
    """
    删除区域公司 修改删除时间
    :param db:
    :param sec:
    :param sub_id:
    :return:
    """
    from datetime import datetime
    response = db.query(RegionCompany).filter(
        RegionCompany.sub_id == sub_id, RegionCompany.sec_id.in_(sec), RegionCompany.deleted_at.is_(None)
    ).update({"deleted_at": datetime.now()})
    db.commit(), db.close()
    return response
