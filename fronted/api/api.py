import os

from aiohttp import ClientSession
from dotenv import load_dotenv

load_dotenv()
BASE_URL = os.getenv("URL")


async def login(data: dict[str:str], session: ClientSession):
    """
    получить токен
    """
    response = await session.post(f"{BASE_URL}/auth/token", data=data)
    if response.status == 200:
        return await response.json()
    raise


async def register(data: dict[str:str], session: ClientSession) -> int:
    """
    зарегистрироваться
    """
    response = await session.post(f"{BASE_URL}/auth/register", params=data)
    if response.status == 200:
        return await response.json()
    raise


async def get_hundred(session: ClientSession, access_token: str, refresh_token: str):
    """
    получить топ 100 монет
    """
    data = (401, None)
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
        resp = await session.post(
            f"{BASE_URL}/auth/refresh",
            headers={"Authorization": f"Bearer {refresh_token}"},
        )
        if resp.status == 200:
            result = await resp.json()
            data = await get_hundred(
                session, result["access_token"], result["refresh_token"]
            )
        elif resp.status == 401:
            return 401, None
    return data


async def change_password(
    session: ClientSession, access_token: str, refresh_token: str
):
    """
    сменить пароль
    """
    response = await session.patch(
        f"{BASE_URL}/users/patch_user_password",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    if response.status == 200:
        return await response.json()
    return response.status
