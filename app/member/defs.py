from ..admin.auth.schemas import TokenData


def verification_sub_id(mode, user: TokenData):
    """验证接收体sub id 与 授权 sub id"""
    if mode.sub_id:
        mode.sub_id = user.sub_id
    return mode
