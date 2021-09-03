from fastapi import APIRouter
from .users.main import router as user_router
from .plans.main import router as plan_router
from .ages.main import router as age_router
from .sources.main import router as source_router
from .types.main import router as type_router
from .qualities.main import router as quality_router

router = APIRouter(prefix='/member')

router.include_router(age_router, prefix='/ages', tags=['Member Ages'])
router.include_router(source_router, prefix='/sources', tags=['Member Sources'])
router.include_router(type_router, prefix='/types', tags=['Member Types'])
router.include_router(quality_router, prefix='/qualities', tags=['Member Qualities'])
router.include_router(user_router, prefix='/users', tags=['Member Users'])
router.include_router(plan_router, prefix='/plans', tags=['Member Plans'])
