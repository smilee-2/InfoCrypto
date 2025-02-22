from fastapi import APIRouter

router = APIRouter(prefix='/coins', tags=['Coins'])


@router.get('/')
async def get_crypto():
    ...


@router.get('/{id}')
async def get_crypto_one(id: int):
    ...