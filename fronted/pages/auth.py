from pathlib import Path

import flet as ft
from aiohttp import ClientSession

from fronted.api.api import login, register
from fronted.pages import routers


async def auth_page(page: ft.Page, session: ClientSession):
    """
    Страница Авторизации
    """

    page.clean()

    async def login_req(e):
        if "" in (login_field.value, password_field.value):
            print("поля пустые")
            return
        data_user = {"username": login_field.value, "password": password_field.value}
        password_field.value = ""
        login_field.value = ""
        page.update()
        response = await login(data_user, session)
        if response == 401:
            return
        await page.client_storage.set_async("access_token", response["access_token"])
        await page.client_storage.set_async("refresh_token", response["refresh_token"])
        access_token = await page.client_storage.get_async("access_token")
        if access_token:
            await routers.PAGES.get("basic")(page, session)

    async def register_req(e):
        if password_field.value != conf_password_field.value:
            print("passwords !=")
            return
        if "" in (
            email_field.value,
            login_field.value,
            password_field.value,
            conf_password_field.value,
        ):
            print("поля пустые")
            return
        data_user = {
            "email": email_field.value,
            "username": login_field.value,
            "password": password_field.value,
        }
        email_field.value = ""
        password_field.value = ""
        login_field.value = ""
        conf_password_field.value = ""
        await register(data_user, session)
        await login_req(e)

    async def register_page(e):
        page.clean()
        login_btn.on_click = login_page
        signup_btn.on_click = register_req
        page.add(
            ft.Stack([background, main_area_register], alignment=ft.alignment.center)
        )
        page.update()

    async def login_page(e):
        page.clean()
        access_token = await page.client_storage.get_async("access_token")
        if access_token:
            await routers.PAGES.get("basic")(page, session)
        else:
            login_btn.on_click = login_req
            signup_btn.on_click = register_page
            page.add(
                ft.Stack([background, main_area_login], alignment=ft.alignment.center)
            )
            page.update()

    # Fields and buttons
    email_field = ft.TextField(
        label="Email",
        width=500,
        max_lines=900,
        border_width=1,
        color=ft.Colors.WHITE,
        border_color=ft.Colors.WHITE,
        cursor_color=ft.Colors.WHITE,
        label_style=ft.TextStyle(color=ft.Colors.WHITE),
    )
    login_field = ft.TextField(
        label="Login",
        width=500,
        max_lines=900,
        border_width=1,
        color=ft.Colors.WHITE,
        border_color=ft.Colors.WHITE,
        cursor_color=ft.Colors.WHITE,
        label_style=ft.TextStyle(color=ft.Colors.WHITE),
    )
    password_field = ft.TextField(
        label="password",
        width=500,
        max_lines=900,
        password=True,
        border_width=1,
        color=ft.Colors.WHITE,
        border_color=ft.Colors.WHITE,
        cursor_color=ft.Colors.WHITE,
        label_style=ft.TextStyle(color=ft.Colors.WHITE),
    )
    conf_password_field = ft.TextField(
        label="Confirm password",
        width=500,
        max_lines=900,
        password=True,
        border_width=1,
        color=ft.Colors.WHITE,
        border_color=ft.Colors.WHITE,
        cursor_color=ft.Colors.WHITE,
        label_style=ft.TextStyle(color=ft.Colors.WHITE),
    )
    login_btn = ft.OutlinedButton(
        text="Войти",
        width=200,
        height=50,
        style=ft.ButtonStyle(
            side=ft.BorderSide(1, ft.Colors.WHITE), color=ft.Colors.WHITE
        ),
    )
    signup_btn = ft.OutlinedButton(
        text="Зарегистрироваться",
        width=200,
        height=50,
        style=ft.ButtonStyle(
            side=ft.BorderSide(1, ft.Colors.WHITE), color=ft.Colors.WHITE
        ),
    )
    main_column_login = ft.Column(
        controls=[
            ft.Row([login_field], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([password_field], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([login_btn, signup_btn], alignment=ft.MainAxisAlignment.CENTER),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    )
    main_column_register = ft.Column(
        controls=[
            ft.Row([email_field], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([login_field], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([password_field], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([conf_password_field], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([login_btn, signup_btn], alignment=ft.MainAxisAlignment.CENTER),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    )
    main_area_login = ft.Container(
        padding=10,
        border=ft.border.all(1, ft.Colors.WHITE),
        border_radius=10,
        bgcolor=ft.Colors.with_opacity(0, ft.Colors.WHITE),
        content=main_column_login,
        width=700,
        height=900,
        blur=ft.Blur(sigma_x=10, tile_mode=ft.BlurTileMode.MIRROR, sigma_y=10),
    )
    main_area_register = ft.Container(
        padding=10,
        border=ft.border.all(1, ft.Colors.WHITE),
        border_radius=10,
        bgcolor=ft.Colors.with_opacity(0, ft.Colors.WHITE),
        content=main_column_register,
        width=700,
        height=900,
        blur=ft.Blur(sigma_x=10, tile_mode=ft.BlurTileMode.MIRROR, sigma_y=10),
    )
    background = ft.Container(
        width=page.width,
        height=page.height,
        image=ft.DecorationImage(src=r"/bg_auth.png"),
        margin=-100,
        alignment=ft.alignment.center_right,
        expand=True,
    )

    page.update()
    page.appbar = None
    await login_page(None)
