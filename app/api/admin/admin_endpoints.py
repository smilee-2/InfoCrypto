from fastapi import APIRouter, HTTPException, status

from ..models import UserModel
from app.core.database.crud import UserCrud

router = APIRouter(prefix='/admin', tags=['Admin'])


@router.get('/get_user_by_id/{user_id}')
async def get_user_by_id(user_id: int) -> UserModel:
    """эндпоинт вернет пользователя по id"""
    return await UserCrud.get_user_by_id(user_id=user_id)


@router.get('/get_user_by_username/{username}')
async def get_user_by_username(username: str) -> UserModel:
    """эндпоинт вернет пользователя по имени"""
    return await UserCrud.get_user_by_username(username=username)


@router.delete('/delete_user/{username}')
async def delete_user(username: str) -> bool:
    """эндпоинт удалит пользователя"""
    try:
        return await UserCrud.delete_user(username=username)
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='user not found')


@router.patch('/disable_user/{username}')
async def disable_user(username: str):
    """эндпоинт заблокирует пользователя"""
    ...