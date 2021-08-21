from fastapi import Depends, Security, HTTPException
from fastapi.security import SecurityScopes, OAuth2PasswordBearer
from sqlalchemy.orm import Session

from .defs import read_config, token_verify_password, token_payload, hashids_encode, hashids_decode, dbs
from .schemas import AuthUserOut, User, TokenData

SECRET_KEY = read_config('oauth', 'SECRET_KEY')
ALGORITHM = read_config('oauth', 'ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = read_config('oauth', 'ACCESS_TOKEN_EXPIRE_MINUTES')

HASHIDS_SALT = read_config('oauth', 'HASHIDS_SALT')
HASHIDS_LENGTH = read_config('oauth', 'HASHIDS_LENGTH')
HASHIDS_ALPHABET = read_config('oauth', 'HASHIDS_ALPHABET')

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/admin/auth/token",
    scopes={"admin": "all permissions."}
)


def authenticate_user(db: Session, username: str, password: str):
    """
    验证用户信息
    :param db:
    :param username:
    :param password:
    :return:
    """
    from .crud import auth_user_by_username_and_available
    user = auth_user_by_username_and_available(db=db, username=username)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    hashids = hashids_encode(user.id, salt=HASHIDS_SALT, min_length=HASHIDS_LENGTH, alphabet=HASHIDS_ALPHABET)
    if not user.sub_id:
        raise HTTPException(status_code=400, detail="Incorrect sub")
    sub_hashids = hashids_encode(user.sub_id, salt=HASHIDS_SALT, min_length=HASHIDS_LENGTH, alphabet=HASHIDS_ALPHABET)
    user = AuthUserOut(**user.to_dict(), hashids=hashids, sub_hashids=sub_hashids)
    if not token_verify_password(plain_password=password, hashed_password=user.password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    # user = {
    #     "username": "alice",
    #     "password": "$2b$12$jZk8.WpxtbnhX9juSjoGiuNJEAPtdM2h2fl.x998XgNMCk5OLTWXW",
    #     "disabled": False,
    # }
    # user = UserInDB(**user)
    return user


def token_authenticate_access_token(db, username: str, password: str, scopes: list):
    """
    认证用户且生成用户token
    :param db:
    :param username:
    :param password:
    :param scopes:
    :return:
    """
    from datetime import timedelta
    from .defs import token_access_token
    user = authenticate_user(db=db, username=username, password=password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    return token_access_token(
        data={"sub": user.username, "hashids": user.hashids, "sub_hashids": user.sub_hashids, "scopes": scopes},
        key=SECRET_KEY,
        algorithm=ALGORITHM,
        expires_delta=access_token_expires
    )


async def current_user_security(security_scopes: SecurityScopes, token: str = Depends(oauth2_scheme)):
    """
    解析加密字段
    :param security_scopes:
    :param token:
    :return:
    """
    payload = token_payload(security_scopes, token, SECRET_KEY, ALGORITHM)
    user_id, = hashids_decode(payload['hashids'], salt=HASHIDS_SALT, min_length=HASHIDS_LENGTH,
                              alphabet=HASHIDS_ALPHABET)
    sub_id, = hashids_decode(payload['sub_hashids'], salt=HASHIDS_SALT, min_length=HASHIDS_LENGTH,
                             alphabet=HASHIDS_ALPHABET)
    """处理授权用户实时情况"""
    # Todo
    """处理授权用户实时情况"""
    return TokenData(**payload, username=payload['sub'], user_id=user_id, sub_id=sub_id)


async def auth_user(user: TokenData = Security(current_user_security, scopes=['admin']), db: Session = Depends(dbs)):
    """
    demo
    :param user:
    :param db:
    :return:
    """
    from .crud import auth_user_by_username_and_available
    user = auth_user_by_username_and_available(db=db, username=user.username)
    return user
