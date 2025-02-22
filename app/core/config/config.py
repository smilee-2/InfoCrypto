import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

BASE_DIR = Path(__file__).parent.parent.parent.parent
load_dotenv()

class Setting(BaseSettings):
    db_url: str = f"sqlite+aiosqlite:///{BASE_DIR}/database/database.db"
    db_echo: bool = True

    coin_api_key = os.getenv('COIN_API')

setting = Setting()

engine = create_async_engine(
    url=setting.db_url,
    echo=setting.db_echo
)

session_maker = async_sessionmaker(engine, expire_on_commit=False)
