from sqlalchemy import select, delete

from app.core.config.config import session_maker
from app.core.database.schemas import UserSchemas, CoinsFavoritesSchemas
from app.api.models import UserModel


class UsersCrud:
    @staticmethod
    async def create_user(user: UserModel) -> bool:
        """Функция добавит нового пользователя в БД"""
        async with session_maker.begin() as session:
            user = UserSchemas(**user.model_dump())
            session.add(user)
            return True

    @staticmethod
    async def get_user_by_id(user_id: int) -> UserSchemas | None:
        """Вернет пользователя по id"""
        async with session_maker.begin() as session:
            return await session.get(UserSchemas, user_id)

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


class CoinsCrud:
    ...
