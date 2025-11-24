from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model

from organizational_ticking_api.users.selectors.users_selectors import (
    get_active_user_by_id,
    get_active_user_by_username,
)

User = get_user_model()


def auth_login_service(validated_data: dict):
    user = get_active_user_by_username(username=validated_data.get("username"))
    if user is None or not user.check_password(
        raw_password=validated_data.get("password")
    ):
        raise AuthenticationFailed(
            _("invalid credentials. please check your username and password.")
        )
    return get_tokens_for_user_service(user=user)


def get_tokens_for_user_service(user: User) -> dict:
    """
    Get tokens for a user
    Args:
        user (BaseUser): The user to get tokens for.
    Returns:
        dict: The tokens for the user.
    """

    refresh = RefreshToken.for_user(user)
    return {
        "access_token": str(refresh.access_token),
        "refresh_token": str(refresh),
    }


def refresh_user_token_service(refresh_token: RefreshToken):
    """
    Refresh user token
    Args:
        refresh_token (RefreshToken): The refresh token to refresh.
    Returns:
        dict: The refreshed tokens.
    Raises:
        AuthenticationFailed: If the refresh token is invalid.
    """
    try:
        refresh = RefreshToken(refresh_token)
        user_id = int(refresh["user_id"])
        user = get_active_user_by_id(user_id=user_id)
        if user is None:
            raise AuthenticationFailed(_("user not found."))
        token = {
            "refresh_token": str(refresh),
            "access_token": str(refresh.access_token),
        }
        return token
    except (TokenError, InvalidToken, KeyError):
        raise AuthenticationFailed(
            _("invalid credentials. please check your username and password.")
        )
