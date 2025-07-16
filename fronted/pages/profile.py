import flet as ft
from aiohttp import ClientSession

from fronted.api.api import get_favorite_coins, delete_coin
from fronted.pages import routers


async def profile_page(page: ft.Page, session: ClientSession):
    page.clean()
    page.update()

    async def data_processing(e, result):
        page.clean()
        coins = result["coins"]
        if result:
            data = []
            main_info = {}
            count = 1
            for i in coins:
                main_info["id"] = count
                main_info["Name"] = i["coin_name"]
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
                    ft.IconButton(ft.Icons.DELETE_FOREVER),
                    disabled=True,
                    heading_row_alignment=ft.MainAxisAlignment.CENTER,
                )
            )
            rows = []
            for item in data:
                btn_delete = ft.IconButton(
                    icon=ft.Icons.DELETE,
                    on_click=lambda event, row=item: page.run_task(
                        delete_favorite_coin, event, row
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
                            btn_delete,
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
            page.add(
                ft.Stack([background, result_control], alignment=ft.alignment.center)
            )
            page.update()

    async def go_auth_page():
        page.clean()
        await page.client_storage.clear_async()
        await routers.PAGES.get("auth")(page, session)

    async def get_favorite(e):
        access_token = await page.client_storage.get_async("access_token")
        refresh_token = await page.client_storage.get_async("refresh_token")
        if access_token:
            result, tokens = await get_favorite_coins(
                session, access_token, refresh_token
            )
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

    async def delete_favorite_coin(e, row: dict):
        access_token = await page.client_storage.get_async("access_token")
        refresh_token = await page.client_storage.get_async("refresh_token")
        if access_token:
            result, tokens = await delete_coin(
                session, access_token, refresh_token, row["Name"]
            )
            if result == 401:
                await go_auth_page()
                return
            else:
                result = await get_favorite(e)
                await data_processing(e, result)
        else:
            await go_auth_page()
            return

    async def go_profile_page(e):
        result = await get_favorite(e)
        await data_processing(e, result)

    # Fields
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

    await go_profile_page(None)
