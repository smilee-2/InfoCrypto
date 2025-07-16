import flet as ft
from aiohttp import ClientSession

from fronted.api.api import change_password, change_email


async def settings_page(page: ft.Page, session: ClientSession):
    page.clean()
    page.update()

    async def req_change_password(e):
        if old_password_filed.value == new_password_field.value:
            alert_d.content = ft.Text("Новый пароль совпадает со старым")
            page.open(alert_d)
            return
        if "" in (old_password_filed.value, new_password_field.value):
            alert_d.content = ft.Text("Поля для смены пароля не заполнены")
            page.open(alert_d)
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
        if new_email_field.value == "":
            alert_d.content = ft.Text("Поле email не заполнено")
            page.open(alert_d)
            return
        access_token = await page.client_storage.get_async("access_token")
        refresh_token = await page.client_storage.get_async("refresh_token")
        if access_token:
            await change_email(
                session,
                access_token,
                refresh_token,
                {"new_email": new_email_field.value},
            )

    alert_d = ft.AlertDialog(
        title=ft.Text("Ошибка"),
        content=ft.Text("Поля не заполнены"),
        alignment=ft.alignment.center,
        title_padding=ft.padding.all(25),
    )

    old_password_filed = ft.TextField(
        label="Старый пароль",
        password=True,
        width=500,
        max_lines=900,
        border_width=1,
        color=ft.Colors.WHITE,
        border_color=ft.Colors.WHITE,
        cursor_color=ft.Colors.WHITE,
        label_style=ft.TextStyle(color=ft.Colors.WHITE),
    )
    new_password_field = ft.TextField(
        label="Новый пароль",
        password=True,
        width=500,
        max_lines=900,
        border_width=1,
        color=ft.Colors.WHITE,
        border_color=ft.Colors.WHITE,
        cursor_color=ft.Colors.WHITE,
        label_style=ft.TextStyle(color=ft.Colors.WHITE),
    )

    password_change_btn = ft.OutlinedButton(
        text="Сменить пароль",
        on_click=req_change_password,
        width=200,
        height=50,
        style=ft.ButtonStyle(
            side=ft.BorderSide(1, ft.Colors.WHITE), color=ft.Colors.WHITE
        ),
    )

    new_email_field = ft.TextField(
        label="Новая почта",
        width=500,
        max_lines=900,
        border_width=1,
        color=ft.Colors.WHITE,
        border_color=ft.Colors.WHITE,
        cursor_color=ft.Colors.WHITE,
        label_style=ft.TextStyle(color=ft.Colors.WHITE),
    )

    new_email_btn = ft.OutlinedButton(
        text="Сменить почту",
        on_click=change_mail,
        width=200,
        height=50,
        style=ft.ButtonStyle(
            side=ft.BorderSide(1, ft.Colors.WHITE), color=ft.Colors.WHITE
        ),
    )

    main_area = ft.Container(
        content=ft.Column(
            controls=[
                ft.Column(
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
                    spacing=10,
                ),
                ft.Column(
                    controls=[
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
                    spacing=10,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=80,
        ),
        padding=10,
        border=ft.border.all(1, ft.Colors.WHITE),
        border_radius=10,
        bgcolor=ft.Colors.with_opacity(0, ft.Colors.WHITE),
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

    page.add(ft.Stack([background, main_area], alignment=ft.alignment.center))
