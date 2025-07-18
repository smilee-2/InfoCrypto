import os

from dotenv import load_dotenv
from fastapi.security import HTTPBearer
from pydantic_settings import BaseSettings
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

load_dotenv()
HTTP_BEARER = HTTPBearer(auto_error=False)


class SettingDatabase(BaseSettings):
    # for database
    DB_USER: str = os.getenv("DB_USER")
    DB_PASS: str = os.getenv("DB_PASS")
    DB_HOST: str = os.getenv("DB_HOST")
    DB_PORT: int = int(os.getenv("DB_PORT"))
    DB_NAME: str = os.getenv("DB_NAME")
    echo: bool = False

    @property
    def database_url_asyncpg(self):
        # postgres:123@pg:5432
        # {self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}
        return f"postgresql+asyncpg://postgres:123@pg:5432/{self.DB_NAME}"


class SettingCMC(BaseSettings):
    # for crypto cmc
    coin_api_key: str = os.getenv("COIN_API")
    cmc_url: str = "https://pro-api.coinmarketcap.com"


class SettingToken(BaseSettings):
    # for token
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7


setting_db = SettingDatabase()
setting_cmc = SettingCMC()
setting_token = SettingToken()

engine = create_async_engine(url=setting_db.database_url_asyncpg, echo=setting_db.echo)

session_maker = async_sessionmaker(engine, expire_on_commit=False)
