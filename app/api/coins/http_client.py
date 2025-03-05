from aiohttp import ClientSession

from app.core.config.config import setting_cmc


class HTTPClient:
    def __init__(self, base_url: str, headers: dict):
        self._session = ClientSession(
            base_url=base_url,
            headers=headers
        )


class CMCHTTPClient(HTTPClient):
    async def get_listing(self):
        """Вернет список всех активных криптовалют с последними рыночными данными."""
        async with self._session as session:
            async with session.get('/v1/cryptocurrency/listings/latest') as response:
                result = await response.json()
        return result['data']

    async def get_currency(self, currency_id: int):
        """Вернет последнюю рыночную котировку для 1 криптовалюты."""
        async with self._session as session:
            async with session.get(
                    url='/v2/cryptocurrency/quotes/latest',
                    params={'id': currency_id}
            ) as response:
                result = await response.json()
        return result['data'][str(currency_id)]


async def get_obj_cmc() -> CMCHTTPClient:
    """Вернет объект класса CMCHTTPClient"""
    cmc_client = CMCHTTPClient(
    base_url=setting_cmc.cmc_url,
    headers={
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': f'{setting_cmc.coin_api_key}',
    }
    )
    return cmc_client