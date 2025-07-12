import flet as ft
from aiohttp import ClientSession

from fronted.api.api import get_hundred
from fronted.pages import routers


async def basic_page(page: ft.Page, session: ClientSession):
    page.clean()

    async def get_top_coins():
        access_token = await page.client_storage.get_async("access_token")
        refresh_token = await page.client_storage.get_async("refresh_token")
        if access_token:
            result, tokens = await get_hundred(session, access_token, refresh_token)
            if result == 401:
                page.clean()
                await page.client_storage.clear_async()
                await routers.PAGES.get("auth")(page, session)
            else:
                await page.client_storage.set_async(
                    "access_token", tokens["access_token"]
                )
                await page.client_storage.set_async(
                    "refresh_token", tokens["refresh_token"]
                )
                return result
        else:
            page.clean()
            await page.client_storage.clear_async()
            await routers.PAGES.get("auth")(page, session)

    async def go_basic_page(e):
        result = await get_top_coins()
        if result:
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
                ft.DataColumn(ft.Text(key.capitalize())) for key in data[0].keys()
            ]
            rows = []
            for item in data:
                row_cells = [ft.DataCell(ft.Text(value)) for value in item.values()]
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
            page.add(
                ft.Stack([background, result_control], alignment=ft.alignment.center)
            )
            page.update()

    async def go_profile(e):
        await routers.PAGES.get("profile")(page, session)

    async def logout(e):
        await page.client_storage.clear_async()
        page.appbar = None
        await routers.PAGES.get("auth")(page, session)

    async def go_settings(e):
        await routers.PAGES.get("settings")(page, session)

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
        data_row_max_height=30,
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

    await go_basic_page(None)
