import flet as ft
from aiohttp import ClientSession

from fronted.api.api import change_password, change_email


async def settings_page(page: ft.Page, session: ClientSession):
    page.clean()

    async def req_change_password(e):
        if old_password_filed.value == new_password_field.value:
            print("password !=")
            return
        access_token = await page.client_storage.get_async("access_token")
        refresh_token = await page.client_storage.get_async("refresh_token")
        if access_token:
            await change_password(
                session,
                access_token,
                refresh_token,
                {
                    "password": old_password_filed.value,
                    "new_password": new_password_field.value,
                },
            )

    async def change_mail(e):
        access_token = await page.client_storage.get_async("access_token")
        refresh_token = await page.client_storage.get_async("refresh_token")
        if access_token:
            if new_email_field.value != "":
                await change_email(
                    session,
                    access_token,
                    refresh_token,
                    {"new_email": new_email_field.value},
                )

    old_password_filed = ft.TextField(
        label="Старый пароль", width=400, height=80, max_lines=900, password=True
    )
    new_password_field = ft.TextField(
        label="Новый пароль", width=400, height=80, max_lines=900, password=True
    )

    password_change_btn = ft.ElevatedButton(
        text="Сменить пароль", on_click=req_change_password, width=200, height=50
    )

    new_email_field = ft.TextField(
        label="Новая почта",
        width=400,
        height=80,
        max_lines=900,
    )

    new_email_btn = ft.ElevatedButton(
        text="Сменить почту", on_click=change_mail, width=200, height=50
    )

    main_area = ft.Container(
        content=ft.Column(
            controls=[
                ft.Row(
                    [old_password_filed],
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Row(
                    [new_password_field],
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Row(
                    [password_change_btn],
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Row(
                    [new_email_field],
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Row(
                    [new_email_btn],
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        border_radius=10,
        bgcolor=ft.Colors.BLUE_GREY_900,
        width=800,
        height=1000,
        padding=10,
        margin=10,
    )

    page.add(main_area)
