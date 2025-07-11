import asyncio

import flet as ft
from aiohttp import ClientSession

from pages.auth import auth_page
from pages.basic import basic_page


async def main(page: ft.Page):
    page.clean()
    session = ClientSession()
    page.title = "InfoCrypto"
    page.vertical_alignment = ft.MainAxisAlignment.END
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    async def auth(e):
        print("main")
        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        await auth_page(page, session)

    async def on_disconnect(e): ...

    page.on_disconnect = on_disconnect
    access_token = await page.client_storage.get_async("access_token")
    if access_token:
        await basic_page(page, session)
    else:
        await auth(None)


if __name__ == "__main__":
    ft.app(target=main, port=54500, view=ft.AppView.WEB_BROWSER)
