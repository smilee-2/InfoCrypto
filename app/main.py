from contextlib import asynccontextmanager

import uvicorn
from redis import asyncio as aioredis
from fastapi import FastAPI, Depends
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from app.api import router_auth, router_admin, router_coins, router_users
from app.core.config.config import HTTP_BEARER


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = aioredis.from_url("redis://localhost:6379")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield


app = FastAPI(lifespan=lifespan, dependencies=[Depends(HTTP_BEARER)])
app.include_router(router_auth)
app.include_router(router_admin)
app.include_router(router_coins)
app.include_router(router_users)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
