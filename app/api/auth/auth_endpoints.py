from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.api.depends import depends
from app.api.models import UserModel, Token, UserRootModel
from app.core.config.config import setting_token
from app.core.database.crud import UserCrud
from app.api.depends.depends import get_password_hash, verify_password, create_access_token

router = APIRouter(prefix='/auth', tags=['Auth'])


@router.post('/register')
async def register_new_user(user: UserModel = Depends()) -> dict[str, str]:
    """эндпоинт для регистрации"""
    user_ = UserRootModel(**user.model_dump())
    hashed_password = get_password_hash(user.password)
    user_.password = hashed_password
    return await UserCrud.create_user(user_input=user_)


@router.post('/create_admin')
async def create_admin(admin_root: Annotated[UserRootModel, Depends(depends.get_current_user)], admin: UserRootModel = Depends()) -> dict[str, str]:
    """эндпоинт для регистрации админа"""
    hashed_password = get_password_hash(admin.password)
    admin.password = hashed_password
    return await UserCrud.create_user(user_input=admin)


@router.post("/token")
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    """эндпоинт проверит пользователя и вернет jwt токен"""
    user_except = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = await UserCrud.get_user_by_username(form_data.username)
    if not user:
        raise user_except

    check_password = verify_password(form_data.password, user.password)
    if not check_password:
        raise user_except
    access_token_expires = timedelta(minutes=setting_token.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")
