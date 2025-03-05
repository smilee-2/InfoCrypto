from typing import Annotated

from fastapi import APIRouter, Depends

from .http_client import get_obj_cmc
from ..models import UserModel
from ...core.database.crud import CoinsCrud, UserCrud
from app.api.depends import depends

router = APIRouter(prefix='/coins', tags=['Coins'])


@router.get('/get_top_hundred_coins')
async def get_crypto(user: Annotated[UserModel, Depends(depends.get_current_user)]):
    """Вернет информацию топ 100 монет"""
    cmc = await get_obj_cmc()
    return await cmc.get_listing()


@router.get('/get_coin_by_id/{currency_id}')
async def get_crypto_one(currency_id: int, user: Annotated[UserModel, Depends(depends.get_current_user)]):
    """Вернет информацию об одной монете по id"""
    cmc = await get_obj_cmc()
    return await cmc.get_currency(currency_id=currency_id)


@router.get('/add_coin_to_favorites/{currency_id}')
async def add_coin_to_favorites(currency_id: int, user: Annotated[UserModel, Depends(depends.get_current_user)]) -> dict[str, str]:
    cmc = await get_obj_cmc()
    coin_dict = await cmc.get_currency(currency_id=currency_id)
    user_id = await UserCrud.get_user_id(username=user.username)
    return await CoinsCrud.add_coin(coin_input=coin_dict, user_id=user_id)

# TODO
@router.delete('/delete_coin_from_favorites/{currency_id}')
async def delete_coin_from_favorites(currency_id: int, user: Annotated[UserModel, Depends(depends.get_current_user)]) -> dict[str, str]:
    """удалит монету из избранного"""
    ...