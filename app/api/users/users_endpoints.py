from fastapi import APIRouter, HTTPException, status
from pydantic import EmailStr

from ..models import UserModel
from app.core.database.crud import UserCrud, CoinsCrud
from app.core.depends.depends import verify_password, get_password_hash

router = APIRouter(prefix='/users', tags=['User'])


@router.patch('/patch_user_email/{new_email}')
async def patch_user_email(new_email: EmailStr, username: str) -> bool:
    """эндпоинт обновит email пользователя"""
    user = await UserCrud.get_user_by_username(username)
    return await UserCrud.patch_user_email(email=user.email, new_email=new_email)


@router.patch('/patch_user_password')
async def patch_user_password(user_id: int, password: str, new_password: str):
    """эндпоинт обновит пароль пользователя"""
    user = await UserCrud.get_user_by_id(user_id=user_id)
    hash_new_password = get_password_hash(new_password)
    result = verify_password(password, user.password)
    if result:
        return await UserCrud.patch_user_password(user_id=user_id, password=hash_new_password)
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")