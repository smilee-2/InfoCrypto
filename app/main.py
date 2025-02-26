from contextlib import asynccontextmanager
from pathlib import Path
from typing import Annotated

import uvicorn
from fastapi import FastAPI, Request, Response,Depends, HTTPException, status
from fastapi.templating import Jinja2Templates

from api import router_auth, router_admin, router_coins, router_users
from app.api.depends import depends
from app.api.models import UserModel, UserRootModel
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


templates_auth = Jinja2Templates(directory=f'{BASE_DIR}/fronted/auth_page')
templates_main = Jinja2Templates(directory=f'{BASE_DIR}/fronted/main_page')
templates_user = Jinja2Templates(directory=f'{BASE_DIR}/fronted/user_page')
templates_admin = Jinja2Templates(directory=f'{BASE_DIR}/fronted/admin_page')


@app.get('/', tags=['Main'])
async def main(request: Request):
    return templates_auth.TemplateResponse('index.html', {'request': request})


@app.get('/main_page', tags=['Main'])
async def main_page(request: Request, user: Annotated[UserModel, Depends(depends.get_current_user)]):
    return templates_main.TemplateResponse('index.html', {'request': request})


@app.get('/user_page', tags=['Main'])
async def user_page(request: Request, user: Annotated[UserModel, Depends(depends.get_current_user)]):
    return templates_user.TemplateResponse('index.html', {'request': request})


@app.get('/admin_page', tags=['Main'])
async def admin_page(request: Request, admin: Annotated[UserRootModel, Depends(depends.get_current_user)]):
    if admin.root == 'admin':
        return templates_admin.TemplateResponse('index.html', {'request': request})
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='not admin')

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0')