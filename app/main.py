from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from api import router_auth, router_admin, router_coins
from core.config.config import engine
from core.database.schemas import Base

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as connection:
        #await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router_auth)
app.include_router(router_admin)
app.include_router(router_coins)

@app.get('/', tags=['Main'])
async def main():
    return {'msg': 'hello world'}



if __name__ == '__main__':
    uvicorn.run('main:app')