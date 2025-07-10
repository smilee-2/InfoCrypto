from contextlib import asynccontextmanager
from pathlib import Path
from typing import Annotated

import uvicorn
from fastapi import FastAPI, Request, Depends
from fastapi.security import HTTPBearer
from fastapi.templating import Jinja2Templates

from app.api import router_auth, router_admin, router_coins, router_users
from app.api.depends import depends
from app.api.models import UserModel


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


http_bearer = HTTPBearer(auto_error=False)

app = FastAPI(lifespan=lifespan, dependencies=[Depends(http_bearer)])
app.include_router(router_auth)
app.include_router(router_admin)
app.include_router(router_coins)
app.include_router(router_users)


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost")
