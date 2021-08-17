from fastapi import APIRouter

router = APIRouter(prefix='/member/v1')


@router.get("/")
async def root():
    return {"message": "Hello World"}