from django.urls import path, include

urlpatterns = [
    path(
        "auth/", include("organizational_ticking_api.users.urls.auth", namespace="auth")
    )
]
