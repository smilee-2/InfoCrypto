import os

from aiohttp import ClientSession
from dotenv import load_dotenv

load_dotenv()
BASE_URL = os.getenv("URL")


async def login(data: dict[str:str], session: ClientSession):
    request = await session.post(f"{BASE_URL}/auth/token", data=data)
    if request.status == 200:
        return await request.json()
    raise


async def register(data: dict[str:str], session: ClientSession) -> int:
    request = await session.post(f"{BASE_URL}/auth/register", params=data)
    if request.status == 200:
        return await request.json()
    raise


async def get_hundred(session: ClientSession, access_token: str):
    request = await session.get(
        f"{BASE_URL}/coins/get_top_hundred_coins",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    if request.status == 200:
        return await request.json()
    return request.status
