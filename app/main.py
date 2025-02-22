import uvicorn
from fastapi import FastAPI

from api import router_auth, router_admin, router_coins

app = FastAPI()
app.include_router(router_auth)
app.include_router(router_admin)
app.include_router(router_coins)

@app.get('/', tags=['Main'])
async def main():
    return {'msg': 'hello world'}


if __name__ == '__main__':
    uvicorn.run('main:app')