import os
from functools import wraps

from aiohttp import ClientSession
from dotenv import load_dotenv

load_dotenv()
BASE_URL = os.getenv("URL")


def update_tokens_decorator(func):
    """обновить access через refresh или вернуть 401 error"""

    @wraps(func)
    async def wrapper(*args, **kwargs):
        session, access_token, refresh_token, *ar = args
        result, tokens = await func(session, access_token, refresh_token, *ar)
        answer_iof_refresh = (result, tokens)
        if result == 401:
            resp = await session.post(
                f"{BASE_URL}/auth/refresh",
                headers={"Authorization": f"Bearer {refresh_token}"},
            )
            if resp.status == 200:
                result = await resp.json()
                answer_iof_refresh = await func(
                    session, result["access_token"], result["refresh_token"], *ar
                )
            elif resp.status == 401:
                return 401, None
        return answer_iof_refresh

    return wrapper


### Auth
async def login(data: dict[str:str], session: ClientSession):
    """
    получить токен
    """
    response = await session.post(f"{BASE_URL}/auth/token", data=data)
    if response.status == 200:
        return await response.json()
    return 401


async def register(data: dict[str:str], session: ClientSession):
    """
    зарегистрироваться
    """
    response = await session.post(f"{BASE_URL}/auth/register", params=data)
    if response.status == 200:
        return await response.json()
    return 409


### Coins
class CoinsApi:
    @staticmethod
    @update_tokens_decorator
    async def get_hundred(
        session: ClientSession, access_token: str, refresh_token: str
    ):
        """
        получить топ 100 монет
        """
        answer_iof_refresh = (401, None)
        response = await session.get(
            f"{BASE_URL}/coins/get_top_hundred_coins",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        if response.status == 200:
            return await response.json(), {
                "access_token": access_token,
                "refresh_token": refresh_token,
            }
        elif response.status == 401:
            return answer_iof_refresh
        return answer_iof_refresh

    @staticmethod
    @update_tokens_decorator
    async def get_favorite_coins(
        session: ClientSession, access_token: str, refresh_token: str
    ):
        """
        Получить избранные монеты
        """
        answer_iof_refresh = (401, None)
        response = await session.get(
            f"{BASE_URL}/coins/get_all_favorites_coins",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        if response.status == 200:
            return await response.json(), {
                "access_token": access_token,
                "refresh_token": refresh_token,
            }
        elif response.status == 401:
            return answer_iof_refresh
        return answer_iof_refresh

    @staticmethod
    @update_tokens_decorator
    async def add_fav_coin_in_db(
        session: ClientSession, access_token: str, refresh_token: str, coin_id: int
    ):
        """Добавить монету в избранное"""
        answer_iof_refresh = (401, None)
        response = await session.get(
            f"{BASE_URL}/coins/add_coin_to_favorites/{coin_id}",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        if response.status == 200:
            return await response.json(), {
                "access_token": access_token,
                "refresh_token": refresh_token,
            }
        elif response.status == 401:
            return answer_iof_refresh
        elif response.status == 409:
            return 409, None
        return answer_iof_refresh

    @staticmethod
    @update_tokens_decorator
    async def get_fav_one_coin(
        session: ClientSession, access_token: str, refresh_token: str, coin_id: int
    ):
        """Добавить монету в избранное"""
        answer_iof_refresh = (401, None)
        response = await session.get(
            f"{BASE_URL}/coins/get_coin_by_id/{coin_id}",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        if response.status == 200:
            return await response.json(), {
                "access_token": access_token,
                "refresh_token": refresh_token,
            }
        elif response.status == 401:
            return answer_iof_refresh
        elif response.status == 409:
            return 409, None
        return answer_iof_refresh

    @staticmethod
    @update_tokens_decorator
    async def delete_coin(
        session: ClientSession, access_token: str, refresh_token: str, coin_name: str
    ):
        answer_iof_refresh = (401, None)
        response = await session.delete(
            f"{BASE_URL}/coins/delete_coin_from_favorites",
            headers={"Authorization": f"Bearer {access_token}"},
            params={"coin_name": coin_name},
        )
        if response.status == 200:
            return await response.json(), {
                "access_token": access_token,
                "refresh_token": refresh_token,
            }
        elif response.status == 401:
            return answer_iof_refresh
        return answer_iof_refresh


### Settings
class SettingsApi:

    @staticmethod
    @update_tokens_decorator
    async def change_password(
        session: ClientSession,
        access_token: str,
        refresh_token: str,
        passwords: dict[str:str],
    ):
        """
        сменить пароль
        """
        answer_iof_refresh = (401, None)
        response = await session.patch(
            f"{BASE_URL}/users/patch_user_password",
            headers={"Authorization": f"Bearer {access_token}"},
            params=passwords,
        )
        if response.status == 200:
            return await response.json(), {
                "access_token": access_token,
                "refresh_token": refresh_token,
            }
        elif response.status == 401:
            return answer_iof_refresh
        return answer_iof_refresh

    @staticmethod
    @update_tokens_decorator
    async def change_email(
        session: ClientSession,
        access_token: str,
        refresh_token: str,
        new_email: dict[str:str],
    ):
        """
        сменить почту
        """
        answer_iof_refresh = (401, None)
        response = await session.patch(
            f"{BASE_URL}/users/patch_user_email",
            headers={"Authorization": f"Bearer {access_token}"},
            params=new_email,
        )
        if response.status == 200:
            return await response.json(), {
                "access_token": access_token,
                "refresh_token": refresh_token,
            }
        elif response.status == 401:
            return answer_iof_refresh
        return answer_iof_refresh


### Admin


class AdminApi:
    @staticmethod
    @update_tokens_decorator
    async def get_all_users(
        session: ClientSession,
        access_token: str,
        refresh_token: str,
    ):
        """Получить всех пользователей"""
        answer_iof_refresh = (401, None)
        response = await session.get(
            f"{BASE_URL}/admin/get_all_users",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        if response.status == 200:
            return await response.json(), {
                "access_token": access_token,
                "refresh_token": refresh_token,
            }
        elif response.status == 401:
            return answer_iof_refresh
        elif response.status == 403:
            return 403, None
        return answer_iof_refresh

    @staticmethod
    @update_tokens_decorator
    async def disable_user(
        session: ClientSession, access_token: str, refresh_token: str, username: str
    ):
        """Забанить пользователя"""
        answer_iof_refresh = (401, None)
        response = await session.patch(
            f"{BASE_URL}/admin/disable_user/{username}",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        if response.status == 200:
            return await response.json(), {
                "access_token": access_token,
                "refresh_token": refresh_token,
            }
        elif response.status == 401:
            return answer_iof_refresh
        elif response.status == 403:
            return 403, None
        return answer_iof_refresh

    @staticmethod
    @update_tokens_decorator
    async def enable_user(
        session: ClientSession, access_token: str, refresh_token: str, username: str
    ):
        """Забанить пользователя"""
        answer_iof_refresh = (401, None)
        response = await session.patch(
            f"{BASE_URL}/admin/enable_user/{username}",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        if response.status == 200:
            return await response.json(), {
                "access_token": access_token,
                "refresh_token": refresh_token,
            }
        elif response.status == 401:
            return answer_iof_refresh
        elif response.status == 403:
            return 403, None
        return answer_iof_refresh
