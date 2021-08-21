from fastapi import APIRouter

router = APIRouter()


@router.get('/{pk}')
async def qualities(pk: int):
    pass
