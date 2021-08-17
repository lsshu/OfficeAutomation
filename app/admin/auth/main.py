from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .oauth import current_user, token_authenticate_access_token
from .schemas import Token, User
from .defs import dbs

router = APIRouter(prefix='/v1')


@router.post('/token', response_model=Token)
async def login_for_access_token(db: Session = Depends(dbs), form_data: OAuth2PasswordRequestForm = Depends()):
    access_token = token_authenticate_access_token(
        db=db,
        username=form_data.username,
        password=form_data.password,
        scopes=form_data.scopes
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me", response_model=User)
async def read_users_me(user: User = Depends(current_user)):
    return user
