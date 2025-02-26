from typing import Annotated

from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import EmailStr

from ..models import UserModel
from app.core.database.crud import UserCrud
from app.api.depends.depends import verify_password, get_password_hash
from app.api.depends import depends

router = APIRouter(prefix='/users', tags=['User'])


@router.patch('/patch_user_email/{new_email}')
async def patch_user_email(new_email: EmailStr, user: Annotated[UserModel, Depends(depends.get_current_user)]) -> dict[str, str]:
    """эндпоинт обновит email пользователя"""
    return await UserCrud.patch_user_email(email=user.email, new_email=new_email)


@router.patch('/patch_user_password')
async def patch_user_password(password: str, new_password: str, user: Annotated[UserModel,
    Depends(depends.get_current_user)]) -> dict[str, str]:
    """эндпоинт обновит пароль пользователя"""
    user = await UserCrud.get_user_by_username(username=user.username)
    hash_new_password = get_password_hash(new_password)
    result = verify_password(password, user.password)
    if result:
        return await UserCrud.patch_user_password(username=user.username, password=hash_new_password)
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")