def read_config(group, key, **kwargs):
    """
    读取配置文件
    :param group: 分组 [api]
    :param key: key = value
    :param kwargs: file_path 配置文件路径
    :return: value
    """
    from configparser import ConfigParser
    import os
    conn = ConfigParser()
    file_path = kwargs.get('file_path', os.path.join(os.path.abspath('.'), 'config.ini'))
    if not os.path.exists(file_path):
        raise FileNotFoundError("%s 文件不存在" % file_path)
    conn.read(file_path, encoding="utf8")
    return conn.get(group, key)


def hashids_encode(ids: int, **kwargs):
    """
    hashids 加密
    :param ids:
    :param kwargs:
    :return:
    """
    from hashids import Hashids
    hashids = Hashids(**kwargs)
    return hashids.encode(ids)


def hashids_decode(string: str, **kwargs):
    """
    hashids 解密
    :param string:
    :param kwargs:
    :return:
    """
    from hashids import Hashids
    hashids = Hashids(**kwargs)
    return hashids.decode(string)


def get_mac_address():
    """
    获取 本机 mac 地址
    :return:
    """
    import uuid
    mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
    return ":".join([mac[e:e + 2] for e in range(0, 11, 2)])


def get_host_name():
    """
    获取主机名
    :return:
    """
    import socket
    return socket.getfqdn(socket.gethostname())


def get_host_ip():
    """
    获取IP地址
    :return:
    """
    import socket
    # return socket.gethostbyname(socket.getfqdn(socket.gethostname()))
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip


def dbs():
    """
    实例 sessionmaker
    :return:
    """
    from .db import SessionLocal
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def token_verify_password(plain_password: str, hashed_password: str):
    """
    验证 oauth token密码
    :param plain_password: 明文密码
    :param hashed_password: hash 密码
    :return: bool
    """
    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

    return pwd_context.verify(plain_password, hashed_password)


def token_get_password_hash(password: str):
    """
    给 oauth user 加密
    :param password: 加密密码
    :return: hash
    """
    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
    return pwd_context.hash(password)


def token_access_token(data: dict, key: str, algorithm: str, expires_delta):
    """
    生成 token
    :param data: 加密数据
    :param key: 加密key
    :param algorithm: 加密 算法
    :param expires_delta: 有效期 类型 timedelta
    :return: token
    """
    from datetime import datetime, timedelta
    from jose import jwt
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=15))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(claims=to_encode, key=key, algorithm=algorithm)
    return encoded_jwt


def token_payload(security_scopes, token, key, algorithm):
    """
    获取 当前授权用户数据
    :param security_scopes: SecurityScopes
    :param token: OAuth2PasswordBearer
    :param key: 加密key
    :param algorithm: 加密 算法
    :return:
    """
    from jose import jwt, JWTError
    from fastapi import HTTPException, status
    from pydantic import ValidationError
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = f'Bearer'
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail='Could not validate credentials',
                                          headers={"WWW-Authenticate": authenticate_value})
    try:
        payload = jwt.decode(token=token, key=key, algorithms=[algorithm])
        sub: str = payload.get('sub')
        if sub is None:
            raise credentials_exception
        token_scopes = payload.get("scopes", [])
    except (JWTError, ValidationError):
        raise credentials_exception
    for scope in security_scopes.scopes:
        if scope not in token_scopes:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not enough permissions",
                                headers={"WWW-Authenticate": authenticate_value})
    return payload


def verification_sub_id(mode, user):
    """验证接收体sub id 与 授权 sub id"""
    if not mode.sub_id:
        mode.sub_id = user.sub_id
    return mode
