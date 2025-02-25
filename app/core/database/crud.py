from sqlalchemy import select, delete
from pydantic import EmailStr

from app.core.config.config import session_maker
from app.core.database.schemas import UserSchemas, CoinsFavoritesSchemas
from app.api.models import UserModel


class UserCrud:
    @staticmethod
    async def create_user(user: UserModel) -> bool:
        """Функция добавит нового пользователя в БД"""
        async with session_maker.begin() as session:
            user = UserSchemas(**user.model_dump())
            session.add(user)
            return True

    @staticmethod
    async def get_user_by_id(user_id: int) -> UserModel | None:
        """Вернет пользователя по id"""
        async with session_maker.begin() as session:
            user = await session.get(UserSchemas, user_id)
            return UserModel.model_validate(user)

    @staticmethod
    async def get_user_by_username(username: str) -> UserModel | None:
        """Получение пользователя по имени"""
        async with session_maker.begin() as session:
            query = select(UserSchemas).where(UserSchemas.username == username)
            result = await session.execute(query)
            user = result.scalar_one_or_none()
            if user:
                return UserModel.model_validate(user)
            return None

    @staticmethod
    async def get_user_id(username: str) -> int | None:
        """Получение id пользователя"""
        async with session_maker.begin() as session:
            query = select(UserSchemas).where(UserSchemas.username == username)
            result = await session.execute(query)
            user = result.scalar_one_or_none()
            if user:
                return user.id
            return None

    @staticmethod
    async def delete_user(username: str) -> bool:
        """Удаление пользователя вместе со всеми избранными монетами"""
        async with session_maker.begin() as session:
            query_user = select(UserSchemas).where(UserSchemas.username == username)
            result = await session.execute(query_user)
            user = result.scalar_one_or_none()
            if user:
                query_tasks = delete(CoinsFavoritesSchemas).where(CoinsFavoritesSchemas.user_id == user.id)
                result_tasks = await session.execute(query_tasks)
                await session.delete(user)
                return True
            return False

    @staticmethod
    async def patch_user_email(email: EmailStr, new_email: EmailStr) -> bool:
        """Изменение email пользователя"""
        async with session_maker.begin() as session:
            query_user = select(UserSchemas).where(UserSchemas.email == email)
            result = await session.execute(query_user)
            user = result.scalar_one_or_none()
            if user:
                user.email = new_email
                return True
            return False

    @staticmethod
    async def patch_user_password(user_id: int ,password: str) -> bool:
        """Изменение пароля пользователя"""
        async with session_maker.begin() as session:
            query_user = select(UserSchemas).where(UserSchemas.id == user_id)
            result = await session.execute(query_user)
            user = result.scalar_one_or_none()
            if user:
                user.password = password
                return True
            return False


class CoinsCrud:
    ...
