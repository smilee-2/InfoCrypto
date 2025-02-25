from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends, status

from ..models import UserModel
from app.core.database.crud import UserCrud
from app.api.depends import depends

router = APIRouter(prefix='/admin', tags=['Admin'])


@router.get('/get_user_by_id/{user_id}')
async def get_user_by_id(user_id: int, admin: Annotated[UserModel, Depends(depends.get_current_user)]) -> UserModel:
    """эндпоинт вернет пользователя по id"""
    if admin.root == 'admin':
        return await UserCrud.get_user_by_id(user_id=user_id)
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='not admin')


@router.get('/get_user_by_username/{username}')
async def get_user_by_username(username: str,
                               admin: Annotated[UserModel, Depends(depends.get_current_user)]) -> UserModel:
    """эндпоинт вернет пользователя по имени"""
    if admin.root == 'admin':
        return await UserCrud.get_user_by_username(username=username)
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='not admin')


@router.get('/get_all_users')
async def get_all_users(admin: Annotated[UserModel, Depends(depends.get_current_user)]) -> list:
    """эндпоинт вернет всех пользователей"""
    if admin.root == 'admin':
        return await UserCrud.get_all_users()
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='not admin')


@router.patch('/disable_user/{username}')
async def disable_user(username: str, admin: Annotated[UserModel, Depends(depends.get_current_user)]) -> dict[str, str]:
    """эндпоинт заблокирует пользователя"""
    if admin.root == 'admin':
        return await UserCrud.disable_user(username=username)
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='not admin')


@router.patch('/enable_user/{username}')
async def enable_user(username: str, admin: Annotated[UserModel, Depends(depends.get_current_user)]) -> dict[str, str]:
    """эндпоинт разблокирует пользователя"""
    if admin.root == 'admin':
        return await UserCrud.enable_user(username=username)
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='not admin')


@router.delete('/delete_user/{username}')
async def delete_user(username: str, admin: Annotated[UserModel, Depends(depends.get_current_user)]) -> dict[str, str]:
    """эндпоинт удалит пользователя"""
    if admin.root == 'admin':
        try:
            return await UserCrud.delete_user(username=username)
        except:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='user not found')
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='not admin')
