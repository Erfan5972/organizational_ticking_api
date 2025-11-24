from django.urls import path

from organizational_ticking_api.users.apis.auth import (
    LoginApiView,
    RefreshTokenApiView,
    LogoutApiView,
    RegisterApiView,
)

app_name = "auth"

urlpatterns = [
    path("login/", LoginApiView.as_view(), name="users_login"),
    path("refresh_token/", RefreshTokenApiView.as_view(), name="users_refresh_token"),
    path("logout/", LogoutApiView.as_view(), name="users_logout"),
    path("register/", RegisterApiView.as_view(), name="users_register"),
]
