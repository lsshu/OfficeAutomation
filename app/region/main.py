from fastapi import APIRouter
from .companies.main import router as company_router
from .divisions.main import router as division_router
from .markets.main import router as market_router

router = APIRouter(prefix='/region')

router.include_router(company_router, prefix='/companies', tags=['Region Companies'])
router.include_router(division_router, prefix='/divisions', tags=['Region Divisions'])
router.include_router(market_router, prefix='/markets', tags=['Region Markets'])
