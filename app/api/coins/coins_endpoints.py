from fastapi import APIRouter
from .http_client import get_obj_cmc

router = APIRouter(prefix='/coins', tags=['Coins'])


@router.get('/')
async def get_crypto():
    cmc = await get_obj_cmc()
    return await cmc.get_listing()


@router.get('/{currency_id}')
async def get_crypto_one(currency_id: int):
    cmc = await get_obj_cmc()
    return await cmc.get_currency(currency_id=currency_id)
