import flet as ft
from aiohttp import ClientSession

from fronted.api.api import AdminApi
from fronted.pages import routers


async def admin_page(page: ft.Page, session: ClientSession):
    page.clean()
    page.update()

    async def go_auth_page():
        page.clean()
        await page.client_storage.clear_async()
        await routers.PAGES.get("auth")(page, session)

    async def go_admin_page(e):
        page.clean()
        page.update()
        users = await get_users(e)
        result = await data_processing(e, users)
        page.add(ft.Stack([background, result], alignment=ft.alignment.center))
        page.update()

    async def get_users(e):
        access_token = await page.client_storage.get_async("access_token")
        refresh_token = await page.client_storage.get_async("refresh_token")
        if access_token:
            result, tokens = await AdminApi.get_all_users(
                session, access_token, refresh_token
            )
            if result == 401:
                await go_auth_page()
                return
            elif result == 403:
                page.open(alert_d)
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

    async def disable_user(e, row: dict, btn_en_dis: ft.IconButton):
        access_token = await page.client_storage.get_async("access_token")
        refresh_token = await page.client_storage.get_async("refresh_token")
        if access_token:
            result, tokens = await AdminApi.disable_user(
                session, access_token, refresh_token, row["username"]
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
                btn_en_dis.on_click = lambda event: page.run_task(
                    enable_user, event, row, btn_en_dis
                )
                btn_en_dis.icon = ft.Icons.LOCK
                page.update()
                return result
        else:
            await go_auth_page()
            return

    async def enable_user(e, row: dict, btn_en_dis: ft.IconButton):
        access_token = await page.client_storage.get_async("access_token")
        refresh_token = await page.client_storage.get_async("refresh_token")
        if access_token:
            result, tokens = await AdminApi.enable_user(
                session, access_token, refresh_token, row["username"]
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
                btn_en_dis.on_click = lambda event: page.run_task(
                    disable_user, event, row, btn_en_dis
                )
                btn_en_dis.icon = ft.Icons.LOCK_OPEN
                page.update()
                return result
        else:
            await go_auth_page()
            return

    async def delete_user(e, row: dict):
        access_token = await page.client_storage.get_async("access_token")
        refresh_token = await page.client_storage.get_async("refresh_token")
        if access_token:
            result, tokens = await AdminApi.delete_user(
                session, access_token, refresh_token, row["username"]
            )
            if result == 401:
                await go_auth_page()
                return
            else:
                result = await get_users(e)
                await data_processing(e, result)
                page.update()
        else:
            await go_auth_page()
            return

    async def data_processing(e, result):
        data = []
        states = []
        main_info = {}
        state_info = {}
        count = 1
        for i in result:
            main_info["id"] = count
            main_info["email"] = i["email"]
            main_info["username"] = i["username"]
            main_info["root"] = i["root"]
            state_info["state"] = i["disable"]
            data.append(main_info)
            states.append(state_info)
            main_info = {}
            state_info = {}
            count += 1
        # Columns
        columns = [
            ft.DataColumn(
                ft.Text(key.capitalize(), selectable=True),
                heading_row_alignment=ft.MainAxisAlignment.CENTER,
            )
            for key in data[0].keys()
        ]
        columns.append(
            ft.DataColumn(
                ft.IconButton(ft.Icons.PERM_IDENTITY),
                disabled=True,
                heading_row_alignment=ft.MainAxisAlignment.CENTER,
            )
        )
        columns.append(
            ft.DataColumn(
                ft.IconButton(ft.Icons.DELETE_FOREVER),
                disabled=True,
                heading_row_alignment=ft.MainAxisAlignment.CENTER,
            )
        )
        # Rows
        rows = []
        for item, state in zip(data, states):
            btn_en_dis = ft.IconButton(
                icon=ft.Icons.LOCK_OPEN if not state["state"] else ft.Icons.LOCK,
            )
            btn_en_dis.on_click = lambda event, row=item, btn=btn_en_dis: page.run_task(
                disable_user, event, row, btn
            )
            btn_delete = ft.IconButton(
                icon=ft.Icons.DELETE_FOREVER,
                on_click=lambda event, row=item: page.run_task(delete_user, event, row),
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
                        btn_en_dis,
                        alignment=ft.alignment.center,
                    )
                )
            )
            row_cells.append(
                ft.DataCell(
                    ft.Container(
                        btn_delete,
                        alignment=ft.alignment.center,
                    )
                )
            )
            rows.append(ft.DataRow(cells=row_cells))
        # Table
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
        content=ft.Text("Вы не администратор"),
        alignment=ft.alignment.center,
        title_padding=ft.padding.all(25),
    )

    await go_admin_page(None)
