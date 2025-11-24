from django.urls import path, include

urlpatterns = [
    path(
        "auth/", include("organizational_ticking_api.users.urls.auth", namespace="auth")
    ),
    path(
        "tickets/",
        include("organizational_ticking_api.tickets.urls", namespace="tickets"),
    ),
]
