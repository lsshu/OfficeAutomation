from fastapi import APIRouter
from .schemas import AdminMemberPlan

router = APIRouter()


@router.get('/{pk}', response_model=AdminMemberPlan)
async def plan(pk: int):
    pass
