import flet as ft
from aiohttp import ClientSession

from fronted.api.api import login, register
from fronted.pages import routers


async def auth_page(page: ft.Page, session: ClientSession):
    """
    Страница Авторизации
    # TODO Сделать окно контейнер для красоты, а то сплошной фон
    # TODO Сделать предупреждение когда пароли не совпадают при регистрации
    """
    page.clean()

    async def login_req(e):
        data_user = {"username": login_field.value, "password": password_field.value}
        password_field.value = ""
        login_field.value = ""
        page.update()
        response = await login(data_user, session)
        await page.client_storage.set_async("access_token", response["access_token"])
        await page.client_storage.set_async("refresh_token", response["refresh_token"])
        access_token = await page.client_storage.get_async("access_token")
        if access_token:
            await routers.PAGES.get("basic")(page, session)

    async def register_req(e):
        if password_field.value != conf_password_field.value:
            print("passwords !=")
            return
        data_user = {
            "email": email_field.value,
            "username": login_field.value,
            "password": password_field.value,
        }
        await register(data_user, session)
        await login_req(e)

    async def register_page(e):
        page.clean()
        login_btn.on_click = login_page
        signup_btn.on_click = register_req
        page.add(
            email_field,
            login_field,
            password_field,
            conf_password_field,
            ft.Row([login_btn, signup_btn], alignment=ft.MainAxisAlignment.CENTER),
        )
        page.update()

    async def login_page(e):
        page.clean()
        login_btn.on_click = login_req
        signup_btn.on_click = register_page
        page.add(
            login_field,
            password_field,
            ft.Row([login_btn, signup_btn], alignment=ft.MainAxisAlignment.CENTER),
        )
        page.update()

    # Fields
    email_field = ft.TextField(label="Email", width=500, max_lines=900)
    login_field = ft.TextField(label="Login", width=500, max_lines=900)
    password_field = ft.TextField(label="password", width=500, max_lines=900)
    conf_password_field = ft.TextField(
        label="Confirm password", width=500, max_lines=900
    )
    login_btn = ft.ElevatedButton(text="Войти", width=200, height=50)
    signup_btn = ft.ElevatedButton(text="Зарегистрироваться", width=200, height=50)
    page.appbar = None

    await login_page(None)
