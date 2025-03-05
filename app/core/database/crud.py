from sqlalchemy import select, delete
from pydantic import EmailStr

from app.core.config.config import session_maker
from app.core.database.schemas import UserSchemas, CoinsFavoritesSchemas
from app.api.models import UserRootModel


class UserCrud:
    @staticmethod
    async def create_user(user_input: UserRootModel) -> dict[str, str]:
        """Функция добавит нового пользователя в БД"""
        async with session_maker.begin() as session:
            user = UserSchemas(**user_input.model_dump())
            session.add(user)
            return {'message': 'user was created'}

    @staticmethod
    async def get_user_by_id(user_id: int) -> UserRootModel | None:
        """Вернет пользователя по id"""
        async with session_maker.begin() as session:
            user = await session.get(UserSchemas, user_id)
            return UserRootModel.model_validate(user)

    @staticmethod
    async def get_user_by_username(username: str) -> UserRootModel | dict[str, str]:
        """Получение пользователя по имени"""
        async with session_maker.begin() as session:
            query = select(UserSchemas).where(UserSchemas.username == username)
            result = await session.execute(query)
            user = result.scalar_one_or_none()
            if user:
                return UserRootModel.model_validate(user)
            return {'message': 'user not found'}

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
    async def get_all_users() -> list[UserRootModel]:
        """Вернет всех пользователей"""
        async with session_maker.begin() as session:
            query = select(UserSchemas)
            result = await session.execute(query)
            users = result.scalars().all()
            return [UserRootModel.model_validate(user) for user in users]

    @staticmethod
    async def delete_user(username: str) -> dict[str, str]:
        """Удаление пользователя вместе со всеми избранными монетами"""
        async with session_maker.begin() as session:
            query_user = select(UserSchemas).where(UserSchemas.username == username)
            result = await session.execute(query_user)
            user = result.scalar_one_or_none()
            if user:
                query_tasks = delete(CoinsFavoritesSchemas).where(CoinsFavoritesSchemas.user_id == user.id)
                await session.execute(query_tasks)
                await session.delete(user)
                return {'message': 'user was deleted'}
            return {'message': 'user not found'}

    @staticmethod
    async def patch_user_email(email: EmailStr, new_email: EmailStr) -> dict[str, str]:
        """Изменение email пользователя"""
        async with session_maker.begin() as session:
            query_user = select(UserSchemas).where(UserSchemas.email == email)
            result = await session.execute(query_user)
            user = result.scalar_one_or_none()
            user.email = new_email
            return {'message': 'email has been changed'}

    @staticmethod
    async def patch_user_password(username: str, password: str) -> dict[str, str]:
        """Изменение пароля пользователя"""
        async with session_maker.begin() as session:
            query_user = select(UserSchemas).where(UserSchemas.username == username)
            result = await session.execute(query_user)
            user = result.scalar_one_or_none()
            user.password = password
            return {'message': 'password has been changed'}

    @staticmethod
    async def disable_user(username: str) -> dict[str, str]:
        async with session_maker.begin() as session:
            query_user = select(UserSchemas).where(UserSchemas.username == username)
            result = await session.execute(query_user)
            user = result.scalar_one_or_none()
            user.disabled = True
            return {'message': 'user was disabled'}

    @staticmethod
    async def enable_user(username: str) -> dict[str, str]:
        async with session_maker.begin() as session:
            query_user = select(UserSchemas).where(UserSchemas.username == username)
            result = await session.execute(query_user)
            user = result.scalar_one_or_none()
            user.disabled = False
            return {'message': 'user was enabled'}


class CoinsCrud:
    @staticmethod
    async def add_coin(coin_input: dict, user_id: int) -> dict[str, str]:
        async with session_maker.begin() as session:
            coin = CoinsFavoritesSchemas(coin_name=coin_input['name'], user_id=user_id)
            session.add(coin)
            return {'message': 'coin was added to favorites'}