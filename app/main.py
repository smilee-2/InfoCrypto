from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, Depends

from app.api import router_auth, router_admin, router_coins, router_users
from app.core.config.config import HTTP_BEARER


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


# TODO проверка длины пароля


app = FastAPI(lifespan=lifespan, dependencies=[Depends(HTTP_BEARER)])
app.include_router(router_auth)
app.include_router(router_admin)
app.include_router(router_coins)
app.include_router(router_users)


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost")
