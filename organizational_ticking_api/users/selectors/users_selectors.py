from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import NotFound


User = get_user_model()


def get_active_user_by_username(
    username: str,
) -> User:
    """
    Retrieve an active user by their username.

    Args:
        username (str): The username to search for.

    Returns:
        User: The user instance if found.

    Raises:
        NotFound: If no active user exists with the given username.
    """
    user = User.objects.filter(username=username, is_active=True).first()
    if user:
        return user
    return None


def get_active_user_by_id(user_id: int) -> User:
    """
    Get an active user by their ID.

    Args:
        user_id (int): The ID of the user to retrieve.

    Returns:
        user(BaseUser): The active user with the given ID.

    Raises:
        NotFound: If no active user exists with the given ID.
    """
    try:
        return User.objects.get(id=user_id, is_active=True)
    except User.DoesNotExist:
        raise NotFound(_("user not found."))
