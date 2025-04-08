import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

BASE_DIR = Path(__file__).parent.parent.parent.parent
load_dotenv()

class SettingDatabase(BaseSettings):
    # for database
    db_url: str = f"sqlite+aiosqlite:///{BASE_DIR}/database/database.db"
    db_echo: bool = True


class SettingCMC(BaseSettings):
    #for crypto cmc
    coin_api_key: str = os.getenv('COIN_API')
    cmc_url: str = 'https://pro-api.coinmarketcap.com'


class SettingToken(BaseSettings):
    # for token
    SECRET_KEY: str = os.getenv('SECRET_KEY')
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7


setting_db= SettingDatabase()
setting_cmc = SettingCMC()
setting_token = SettingToken()

engine = create_async_engine(
    url=setting_db.db_url,
    echo=setting_db.db_echo
)

session_maker = async_sessionmaker(engine, expire_on_commit=False)
