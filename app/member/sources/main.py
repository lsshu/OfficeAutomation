from fastapi import APIRouter

router = APIRouter()


@router.get('/{pk}')
async def sources(pk: int):
    pass
