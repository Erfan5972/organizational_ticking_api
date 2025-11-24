from django.urls import path

from organizational_ticking_api.users.apis.auth.login.users_auth_login_apis import (
    LoginApiView,
)

app_name = "auth"

urlpatterns = [
    path("login/", LoginApiView.as_view(), name="users_login"),
]
