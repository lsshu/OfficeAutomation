from typing import List
from fastapi import APIRouter, Depends, Security, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .oauth import auth_user, token_authenticate_access_token, current_user_security
from .schemas import Token, User, AuthUserMeStatusResponse, AuthSubjects, TokenData
from .defs import dbs
from .users.main import router as user_router

router = APIRouter()


@router.post('/token', response_model=Token, tags=['Admin Auth'])
async def login_for_access_token(db: Session = Depends(dbs), form_data: OAuth2PasswordRequestForm = Depends()):
    """
    获取登录授权:
    - **form_data**: 登录数据
    """
    access_token = token_authenticate_access_token(
        db=db,
        username=form_data.username,
        password=form_data.password,
        scopes=form_data.scopes
    )
    return Token(access_token=access_token, token_type="bearer")


@router.get("/user", response_model=AuthUserMeStatusResponse, tags=['Admin Auth'])
async def read_users_me(user: User = Depends(auth_user)):
    """
    获取授权用户信息
    :param user:
    :return:
    """
    return AuthUserMeStatusResponse(data=user)


async def check_authorization(request: Request, user: TokenData = Security(current_user_security, scopes=['admin'])):
    """
    全局依赖
    :param request:
    :param user:
    :return:
    """
    request.state.auth_user = user


router.include_router(user_router, prefix='/users', tags=['Admin Auth User'],
                      # dependencies=[Depends(check_authorization)]
                      )

# @router.get('/subjects', response_model=List[AuthSubjects])
# async def subjects(skip: int = 0, limit: int = 100, db: Session = Depends(dbs),
#                    user: TokenData = Security(current_user_security, scopes=['admin'])):
#     from .crud import get_subjects
#     """
#     获取主体列表信息
#     :param skip:
#     :param limit:
#     :param db:
#     :param user:
#     :return:
#     """
#     # from .crud import auth_user_by_username_and_available
#     # user = auth_user_by_username_and_available(db=db, username=user.username)
#     return get_subjects(db=db, skip=skip, limit=limit)
#
#
# @router.get('/subjects/{pk}', response_model=AuthSubjects)
# async def subject(pk: int, db: Session = Depends(dbs),
#                   user: TokenData = Security(current_user_security, scopes=['admin'])):
#     """
#     获取主体信息
#     :param pk:
#     :param db:
#     :param user:
#     :return:
#     """
#     from .crud import get_subject_by_pk
#     return get_subject_by_pk(db=db, pk=pk)
