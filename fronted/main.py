import flet as ft
from aiohttp import ClientSession

from pages.auth import auth_page
from pages.basic import basic_page


async def main(page: ft.Page):
    page.clean()
    session = ClientSession()
    page.bgcolor = ft.Colors.BLACK  # noqa
    page.title = "InfoCrypto"
    page.vertical_alignment = ft.MainAxisAlignment.END
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.AUTO

    async def auth(e):
        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        await auth_page(page, session)

    access_token = await page.client_storage.get_async("access_token")
    if access_token:
        await basic_page(page, session)
    else:
        await auth(None)


if __name__ == "__main__":
    ft.app(
        target=main,
        view=ft.AppView.WEB_BROWSER,
        assets_dir="../assets",
        port=8220,
        host="0.0.0.0",
    )
