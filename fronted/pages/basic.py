import asyncio
from os import access

import flet as ft
from aiohttp import ClientSession

from fronted.api.api import get_hundred, add_fav_coin_in_db
from fronted.pages import routers


async def basic_page(page: ft.Page, session: ClientSession):
    page.clean()
    page.update()

    async def go_auth_page():
        page.clean()
        await page.client_storage.clear_async()
        await routers.PAGES.get("auth")(page, session)

    async def data_processing(e, result):
        data = []
        main_info = {}
        count = 1
        for i in result:
            main_info["top"] = count
            main_info["id"] = i["id"]
            main_info["name"] = i["name"]
            main_info["symbol"] = i["symbol"]
            main_info["price"] = i["quote"]["USD"]["price"]
            data.append(main_info)
            main_info = {}
            count += 1
        columns = [
            ft.DataColumn(
                ft.Text(key.capitalize(), selectable=True),
                heading_row_alignment=ft.MainAxisAlignment.CENTER,
            )
            for key in data[0].keys()
        ]
        columns.append(
            ft.DataColumn(
                ft.IconButton(ft.Icons.STAR),
                disabled=True,
                heading_row_alignment=ft.MainAxisAlignment.CENTER,
            )
        )
        rows = []
        for item in data:
            btn_favorites = ft.IconButton(
                icon=ft.Icons.ADD,
                on_click=lambda event, row=item: page.run_task(
                    add_favorite_coin, event, row
                ),
            )
            row_cells = [
                ft.DataCell(
                    ft.Container(
                        ft.Text(value, selectable=True),
                        alignment=ft.alignment.center,
                    )
                )
                for value in item.values()
            ]
            row_cells.append(
                ft.DataCell(
                    ft.Container(
                        btn_favorites,
                        alignment=ft.alignment.center,
                    )
                )
            )
            rows.append(ft.DataRow(cells=row_cells))

        table.columns = columns
        table.rows = rows
        scrollable_table.controls = [table]
        result_control = ft.Column(
            [
                ft.Container(
                    content=scrollable_table,
                    expand=True,
                    bgcolor=ft.Colors.with_opacity(0, ft.Colors.WHITE),
                    border=ft.border.all(1, ft.Colors.WHITE),
                    border_radius=10,
                    blur=ft.Blur(
                        sigma_x=10, tile_mode=ft.BlurTileMode.MIRROR, sigma_y=10
                    ),
                    padding=10,
                )
            ],
            expand=True,
        )
        return result_control

    async def get_top_coins():
        access_token = await page.client_storage.get_async("access_token")
        refresh_token = await page.client_storage.get_async("refresh_token")
        if access_token:
            result, tokens = await get_hundred(session, access_token, refresh_token)
            if result == 401:
                await go_auth_page()
                return
            else:
                await page.client_storage.set_async(
                    "access_token", tokens["access_token"]
                )
                await page.client_storage.set_async(
                    "refresh_token", tokens["refresh_token"]
                )
                return result
        else:
            await go_auth_page()
            return

    async def add_favorite_coin(e, row: dict):
        access_token = await page.client_storage.get_async("access_token")
        refresh_token = await page.client_storage.get_async("refresh_token")
        # btn_favorites.icon = ft.Icons.DONE
        # btn_favorites.disabled = True
        if access_token:
            result, tokens = await add_fav_coin_in_db(
                session, access_token, refresh_token, row["id"]
            )
            if result == 401:
                await go_auth_page()
                return
            elif result == 409:
                alert_d.title = ft.Text("Ошибка")
                alert_d.content = ft.Text("Монета уже добавлена")
                page.open(alert_d)
                return
            else:
                await page.client_storage.set_async(
                    "access_token", tokens["access_token"]
                )
                await page.client_storage.set_async(
                    "refresh_token", tokens["refresh_token"]
                )
                alert_d.title = ft.Text("Успех!")
                alert_d.content = ft.Text("Монета добавлена")
                page.open(alert_d)
        else:
            await go_auth_page()
            return

    async def go_basic_page(e):
        page.clean()
        page.update()
        result = await get_top_coins()
        result_control = await data_processing(e, result)
        page.add(ft.Stack([background, result_control], alignment=ft.alignment.center))
        page.update()

    async def go_profile(e):
        await routers.PAGES.get("profile")(page, session)

    async def logout(e):
        await page.client_storage.clear_async()
        page.appbar = None
        await routers.PAGES.get("auth")(page, session)

    async def go_settings(e):
        await routers.PAGES.get("settings")(page, session)

    # Fields
    page.appbar = ft.AppBar(
        leading=ft.Icon(ft.Icons.MONETIZATION_ON),
        leading_width=40,
        title=ft.Text("InfoCrypto"),
        center_title=False,
        bgcolor=ft.Colors.with_opacity(0, ft.Colors.PURPLE_900),
        actions=[
            ft.IconButton(ft.Icons.HOME, on_click=go_basic_page),
            ft.IconButton(ft.Icons.PERSON, on_click=go_profile),
            ft.PopupMenuButton(
                items=[
                    ft.PopupMenuItem(text="Settings", on_click=go_settings),
                    ft.PopupMenuItem(text="Logout", on_click=logout),
                ]
            ),
        ],
    )
    table = ft.DataTable(
        columns=[ft.DataColumn(ft.Text(""))],
        column_spacing=200,
        heading_text_style=ft.TextStyle(size=14, weight=ft.FontWeight.BOLD),
        divider_thickness=1,
        data_row_max_height=60,
        data_row_min_height=40,
        horizontal_lines=ft.border.BorderSide(width=1, color=ft.Colors.WHITE),
    )
    scrollable_table = ft.ListView(
        controls=[table],
        expand=True,
        spacing=0,
        padding=0,
        auto_scroll=False,
    )
    background = ft.Container(
        width=page.width,
        height=page.height,
        image=ft.DecorationImage(src=r"/bg_auth.png"),
        margin=-100,
        alignment=ft.alignment.center_right,
        expand=True,
    )
    alert_d = ft.AlertDialog(
        title=ft.Text("Ошибка"),
        content=ft.Text("Монета уже добавлена"),
        alignment=ft.alignment.center,
        title_padding=ft.padding.all(25),
    )

    await go_basic_page(None)
