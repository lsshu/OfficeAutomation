from sqlalchemy.orm import Session

from .schemas import RegionCompanyCreate, RegionCompanyUpdate
from ..models import RegionCompany


def get_companies(db: Session, skip: int = 0, limit: int = 10, sub_id=None):
    """
    获取 区域公司列表
    :param db:
    :param skip:
    :param limit:
    :param sub_id:
    :return:
    """
    if sub_id:
        return db.query(RegionCompany).filter(
            RegionCompany.sub_id == sub_id, RegionCompany.deleted_at.is_(None)
        ).offset(skip).limit(limit).all()
    return db.query(RegionCompany).filter(
        RegionCompany.deleted_at.is_(None)
    ).offset(skip).limit(limit).all()


def get_paginate_companies(db: Session, skip: int = 0, limit: int = 10, sub_id=None):
    import math
    if sub_id:
        count = db.query(RegionCompany).filter(
            RegionCompany.sub_id == sub_id, RegionCompany.deleted_at.is_(None)
        ).count()
    else:
        count = db.query(RegionCompany).filter(
            RegionCompany.deleted_at.is_(None)
        ).count()

    pages = math.ceil(count / limit)
    return {"total": count, "pages": pages, "skip": skip, "limit": limit,
            "data": get_companies(db=db, skip=skip, limit=limit, sub_id=sub_id)}


def get_company_by_pk(db: Session, pk: int, sub_id=None):
    """
    根据主键 获取区域公司
    :param db:
    :param pk:
    :param sub_id:
    :return:
    """
    if sub_id:
        return db.query(RegionCompany).filter(
            RegionCompany.sub_id == sub_id, RegionCompany.id == pk, RegionCompany.deleted_at.is_(None)
        ).first()
    return db.query(RegionCompany).filter(
        RegionCompany.id == pk, RegionCompany.deleted_at.is_(None)
    ).first()


def get_company_by_name(db: Session, name: str, sub_id=None):
    """
    根据名称 获取区域公司
    :param db:
    :param name:
    :param sub_id:
    :return:
    """
    if sub_id:
        return db.query(RegionCompany).filter(
            RegionCompany.sub_id == sub_id, RegionCompany.name == name, RegionCompany.deleted_at.is_(None)
        ).first()
    return db.query(RegionCompany).filter(
        RegionCompany.name == name, RegionCompany.deleted_at.is_(None)
    ).first()


def create_company(db: Session, company: RegionCompanyCreate, sub_id=None):
    """
    创建 区域公司
    :param db:
    :param company:
    :param sub_id:
    :return:
    """
    db_company = RegionCompany(**company.dict())
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company


def update_company(db: Session, company: RegionCompanyUpdate, pk: int, sub_id=None):
    """
    修改 区域公司
    :param db:
    :param company:
    :param pk:
    :param sub_id:
    :return:
    """
    if sub_id:
        db.query(RegionCompany).filter(
            RegionCompany.sub_id == sub_id, RegionCompany.id == pk, RegionCompany.deleted_at.is_(None)
        ).update(company.dict()), db.commit(), db.close()
        return get_company_by_pk(db=db, pk=pk, sub_id=sub_id)
    db.query(RegionCompany).filter(
        RegionCompany.id == pk, RegionCompany.deleted_at.is_(None)
    ).update(company.dict()), db.commit(), db.close()
    return get_company_by_pk(db=db, pk=pk, sub_id=sub_id)


def delete_company(db: Session, pk: int, sub_id=None):
    """
    删除区域公司 修改删除时间
    :param db:
    :param pk:
    :param sub_id:
    :return:
    """
    from datetime import datetime
    if sub_id:
        response = db.query(RegionCompany).filter(
            RegionCompany.sub_id == sub_id, RegionCompany.id == pk, RegionCompany.deleted_at.is_(None)
        ).update({"deleted_at": datetime.now()})
        db.commit(), db.close()
        return response
    response = db.query(RegionCompany).filter(
        RegionCompany.id == pk, RegionCompany.deleted_at.is_(None)
    ).update({"deleted_at": datetime.now()})
    db.commit(), db.close()
    return response
