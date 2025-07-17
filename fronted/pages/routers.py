from fronted.pages.auth import auth_page
from fronted.pages.basic import basic_page
from fronted.pages.profile import profile_page
from fronted.pages.settings import settings_page
from fronted.pages.admin import admin_page

PAGES = {
    "auth": auth_page,
    "admin": admin_page,
    "basic": basic_page,
    "profile": profile_page,
    "settings": settings_page,
}
