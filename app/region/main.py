from fastapi import APIRouter
from .user.main import router as user_router
from .plan.main import router as plan_router

router = APIRouter(prefix='/region')

router.include_router(user_router, prefix='/users', tags=['Member Users'])
router.include_router(plan_router, prefix='/plans', tags=['Member Plans'])
