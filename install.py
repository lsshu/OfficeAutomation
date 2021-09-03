from app.admin.auth.models import Model, Engine, AuthSubject, AuthUser, AuthRoles, AuthPermissions
from app.region.models import RegionCompany, RegionDivision, RegionMarket
from app.member.models import MemberAgeGroup, MemberSource, MemberType, MemberQualityType, MemberUser

if __name__ == '__main__':
    Model.metadata.create_all(Engine)  # 创建表结构
