from typing import TYPE_CHECKING
from collections.abc import Sequence


from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.authentication import BaseAuthentication, BasicAuthentication

from rest_framework_simplejwt.authentication import JWTAuthentication


def get_auth_header(headers):
    value = headers.get("Authorization")

    if not value:
        return None

    auth_type, auth_value = value.split()[:2]

    return auth_type, auth_value


if TYPE_CHECKING:
    # This is going to be resolved in the stub library
    # https://github.com/typeddjango/djangorestframework-stubs/
    from rest_framework.permissions import _PermissionClass

    PermissionClassesType = Sequence[_PermissionClass]
else:
    PermissionClassesType = Sequence[type[BasePermission]]


class ApiAuthMixin:
    authentication_classes: Sequence[type[BaseAuthentication]] = [
        JWTAuthentication,
        BasicAuthentication,
    ]
    permission_classes: PermissionClassesType = (IsAuthenticated,)
