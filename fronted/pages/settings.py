import flet as ft
from aiohttp import ClientSession


async def settings_page(page: ft.Page, session: ClientSession):
    page.clean()

    async def change_password(e):
        if old_password_filed.value != new_password_field.value:
            print("password !=")
            return
        print("password change")

    async def change_mail(e): ...

    old_password_filed = ft.TextField(
        label="Старый пароль", width=400, height=80, max_lines=900, password=True
    )
    new_password_field = ft.TextField(
        label="Новый пароль", width=400, height=80, max_lines=900, password=True
    )

    password_change_btn = ft.ElevatedButton(
        text="Изменить пароль", on_click=change_password, width=200, height=50
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
            ],
            alignment=ft.alignment.center,
        ),
        border_radius=10,
        bgcolor=ft.Colors.BLUE_GREY_900,
        width=800,
        height=1000,
        padding=10,
        margin=10,
    )

    page.add(main_area)
