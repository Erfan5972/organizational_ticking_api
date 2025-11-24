import logging

from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from django.contrib.auth import get_user_model

from organizational_ticking_api.users.selectors.users_selectors import (
    get_active_user_by_id,
    get_active_user_by_username,
)

logger = logging.getLogger(__name__)
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


def refresh_user_token_service(refresh_token: str):
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


def logout_user_service(refresh_token: str) -> None:
    """
    Blacklist refresh token on logout.

    Args:
        refresh_token (str): The refresh token to blacklist.

    Raises:
        AuthenticationFailed: If token is invalid.
    """
    try:
        token = RefreshToken(refresh_token)
        token.blacklist()  # Mark token as invalid for future use
    except (TokenError, InvalidToken) as e:
        logger.error(e)
        raise AuthenticationFailed(_("invalid or expired token."))


def register_user_service(
    *, username: str, password: str, first_name: str | None, last_name: str | None
) -> dict:
    """
    Register a new user and return JWT tokens.

    Args:
        username: Unique username.
        password: Raw password.
        first_name: Optional first name.
        last_name: Optional last name.

    Returns:
        dict: { access_token, refresh_token }

    Raises:
        ValidationError: if username is taken.
    """

    if get_active_user_by_username(username):
        raise ValidationError({"username": _("username already exists.")})

    try:
        user = User.objects.create(
            username=username,
            first_name=first_name or "",
            last_name=last_name or "",
        )
        user.set_password(password)
        user.save()

        return get_tokens_for_user_service(user)

    except Exception as e:
        logger.error(f"Failed to register user `{username}`: {e}")
        raise ValidationError(_("failed to create user. please try again."))
