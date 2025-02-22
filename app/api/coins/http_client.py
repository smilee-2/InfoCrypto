import os

from aiohttp import ClientSession
from dotenv import load_dotenv

load_dotenv()


class HTTPClient:
    def __init__(self, base_url: str, api: str):
        self._session = ClientSession(
            base_url=base_url,
            headers={
                'Accepts': 'application/json',
                'X-CMC_PRO_API_KEY': f'{api}',
            }
        )
        # https://pro-api.coinmarketcap.com

        parameters = {
            'start': '1',
            'limit': '5000',
            'convert': 'USD'
        }


class CMCHTTPClient(HTTPClient):
    async def get_listing(self):
        """Вернет список всех активных криптовалют с последними рыночными данными."""
        async with self._session.get('/v1/cryptocurrency/listings/latest') as response:
            result = await response.json()
            return result['data']

    async def get_currency(self, currency_id: int):
        """Вернет последнюю рыночную котировку для 1 криптовалюты."""
        async with self._session.get(
                url='/v2/cryptocurrency/quotes/latest',
                params={'id': currency_id}
        ) as response:
            result = await response.json()
            return result['data'][str(currency_id)]
