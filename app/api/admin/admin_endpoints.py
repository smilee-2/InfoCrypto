from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi_cache.decorator import cache
from pydantic import EmailStr

from app.api.models import UserRootModel, UserReturnModel
from app.core.database.crud import UserCrud
from app.api.depends import depends

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/get_user_by_id/{user_id}")
@cache(expire=30)
async def get_user_by_id(
    user_id: int, admin: Annotated[UserRootModel, Depends(depends.get_current_user)]
) -> UserReturnModel | dict[str, str]:
    """эндпоинт вернет пользователя по id"""
    if admin.root == "admin":
        user = await UserCrud.get_user_by_id(user_id=user_id)
        return UserReturnModel.model_validate(user)
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="not admin")


@router.get("/get_user_by_username/{username}")
@cache(expire=30)
async def get_user_by_username(
    username: str, admin: Annotated[UserRootModel, Depends(depends.get_current_user)]
) -> UserReturnModel | dict[str, str]:
    """эндпоинт вернет пользователя по имени"""
    if admin.root == "admin":
        user = await UserCrud.get_user_by_username(username=username)
        return UserReturnModel.model_validate(user)
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="not admin")


@router.get("/get_user_by_email/{email}")
@cache(expire=30)
async def get_user_by_email(
    email: EmailStr, admin: Annotated[UserRootModel, Depends(depends.get_current_user)]
) -> UserReturnModel | dict[str, str]:
    """эндпоинт вернет пользователя по email"""
    if admin.root == "admin":
        user = await UserCrud.get_user_by_email(email=email)
        return UserReturnModel.model_validate(user)
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="not admin")


@router.get("/get_all_users")
@cache(expire=30)
async def get_all_users(
    admin: Annotated[UserRootModel, Depends(depends.get_current_user)],
) -> list[UserReturnModel]:
    """эндпоинт вернет всех пользователей"""
    if admin.root == "admin":
        users = await UserCrud.get_all_users()
        list_users = []
        for user in users:
            list_users.append(UserReturnModel.model_validate(user))
        return list_users
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="not admin")


@router.patch("/disable_user/{username}")
async def disable_user(
    username: str, admin: Annotated[UserRootModel, Depends(depends.get_current_user)]
) -> dict[str, str]:
    """эндпоинт заблокирует пользователя"""
    if admin.root == "admin":
        return await UserCrud.disable_user(username=username)
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="not admin")


@router.patch("/enable_user/{username}")
async def enable_user(
    username: str, admin: Annotated[UserRootModel, Depends(depends.get_current_user)]
) -> dict[str, str]:
    """эндпоинт разблокирует пользователя"""
    if admin.root == "admin":
        return await UserCrud.enable_user(username=username)
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="not admin")


@router.delete("/delete_user/{username}")
async def delete_user(
    username: str, admin: Annotated[UserRootModel, Depends(depends.get_current_user)]
) -> dict[str, str]:
    """эндпоинт удалит пользователя"""
    if admin.root == "admin":
        try:
            return await UserCrud.delete_user(username=username)
        except:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="user not found"
            )
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="not admin")
