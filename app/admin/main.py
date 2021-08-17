from fastapi import APIRouter
from .auth.main import router as auth_router

router = APIRouter(prefix='/admin')

router.include_router(auth_router, prefix='/auth')