from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.coins.http_client import get_obj_cmc
from app.api.models import UserModel
from app.core.database.crud import CoinsCrud, UserCrud
from app.api.depends import depends

router = APIRouter(prefix="/coins", tags=["Coins"])


@router.get("/get_top_hundred_coins")
async def get_crypto(
    user: Annotated[UserModel, Depends(depends.get_current_user)],
):
    """Вернет информацию топ 100 монет"""
    cmc = await get_obj_cmc()
    return await cmc.get_listing()


@router.get("/get_all_favorites_coins")
async def get_all_favorites_coins(
    user: Annotated[UserModel, Depends(depends.get_current_user)],
):
    """Вернет все избранные монеты пользователя"""
    user_id = await UserCrud.get_user_id(username=user.username)
    coins = await CoinsCrud.get_all_f_coins(user_id=user_id)
    return {"coins": coins}


@router.get("/get_coin_by_id/{currency_id}")
async def get_crypto_one(
    currency_id: int, user: Annotated[UserModel, Depends(depends.get_current_user)]
):
    """Вернет информацию об одной монете по id"""
    cmc = await get_obj_cmc()
    return await cmc.get_currency(currency_id=currency_id)


@router.get("/add_coin_to_favorites/{currency_id}")
async def add_coin_to_favorites(
    currency_id: int, user: Annotated[UserModel, Depends(depends.get_current_user)]
) -> dict[str, str]:
    cmc = await get_obj_cmc()
    coin_dict = await cmc.get_currency(currency_id=currency_id)
    user_id = await UserCrud.get_user_id(username=user.username)
    chek_coin = await CoinsCrud.get_coin_by_name(
        coin_name=coin_dict["name"], user_id=user_id
    )
    if chek_coin:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Монета уже добавлена"
        )
    return await CoinsCrud.add_coin(coin_input=coin_dict, user_id=user_id)


@router.delete("/delete_coin_from_favorites")
async def delete_coin_from_favorites(
    coin_name: str, user: Annotated[UserModel, Depends(depends.get_current_user)]
) -> dict[str, str]:
    """удалит монету из избранного"""
    user_id = await UserCrud.get_user_id(username=user.username)
    return await CoinsCrud.delete_favorite_coin(coin_name=coin_name, user_id=user_id)
