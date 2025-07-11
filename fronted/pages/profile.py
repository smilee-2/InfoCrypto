import flet as ft
from aiohttp import ClientSession


async def profile_page(page: ft.Page, session: ClientSession):
    page.clean()

    page.add(ft.Text("profile"))
