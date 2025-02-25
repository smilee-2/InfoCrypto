from typing import Annotated
from datetime import timedelta, datetime, timezone

import jwt
from jwt import InvalidTokenError
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, status, Depends

from app.api.models import TokenData
from app.core.config.config import setting_token
from app.core.database.crud import UserCrud

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    """Вернет хеш пароля"""
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    """Проверит пароль пользователя"""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """Создаст и вернет jwt токен"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, setting_token.SECRET_KEY, algorithm=setting_token.ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    """Проверит текущего пользователя"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    try:
        payload = jwt.decode(token, setting_token.SECRET_KEY, algorithms=[setting_token.ALGORITHM])
        username = payload.get('sub')
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError as e:
        raise credentials_exception
    user = await UserCrud.get_user_by_username(username=token_data.username, )
    if user is None:
        raise credentials_exception
    return user
