from typing import List
from fastapi import APIRouter
from .schemas import AdminMemberUser

router = APIRouter()


@router.get('/', response_model=List[AdminMemberUser])
async def users(user):
    print(user)


@router.post('/', response_model=AdminMemberUser)
async def create_user():
    pass


@router.put('/{pk}', response_model=AdminMemberUser)
async def update_user(pk: int, ):
    pass


@router.patch('/{pk}', response_model=AdminMemberUser)
async def update_user(pk: int, ):
    pass


@router.get('/{pk}', response_model=AdminMemberUser)
async def get_user(pk: int):
    pass


@router.delete('/{pk}')
async def delete_user(pk: int):
    pass
