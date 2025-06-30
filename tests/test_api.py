import pytest
from httpx import AsyncClient, ASGITransport

from app.main import app

@pytest.mark.asyncio
async def test_get_crypto():
    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test/coins', auth=('Den','123')) as ac:
        response = await ac.get('/get_top_hundred_coins', headers={'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJEZW4iLCJ0eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ0NjQwODQ0fQ.2yAeDZcBsYIvvoBeBSSvon_Vk7Kd0EBj1JBI4_yxn7c'})
        print(response)