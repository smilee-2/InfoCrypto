from contextlib import asynccontextmanager
from pathlib import Path

import uvicorn
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from api import router_auth, router_admin, router_coins, router_users
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
app.include_router(router_users)


BASE_DIR = Path(__file__).parent.parent


app.mount('/auth_page', StaticFiles(directory=f'{BASE_DIR}/fronted/auth_page'))
templates_auth = Jinja2Templates(directory=f'{BASE_DIR}/fronted/auth_page')



@app.get('/', tags=['Main'])
async def main(request: Request):
    return templates_auth.TemplateResponse('index.html', {'request': request})



if __name__ == '__main__':
    uvicorn.run('main:app')