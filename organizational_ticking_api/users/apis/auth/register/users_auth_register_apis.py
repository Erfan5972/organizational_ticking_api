import logging
from drf_spectacular.utils import extend_schema

from django.utils.translation import gettext_lazy as _
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError

from organizational_ticking_api.users.apis.auth.register.users_auth_register_serializers import (
    AuthRegisterInputSerializer,
    AuthRegisterOutputSerializer,
)
from organizational_ticking_api.users.constants import AUTH_TAG
from organizational_ticking_api.users.services.auth_services import (
    register_user_service,
)

logger = logging.getLogger(__name__)


class RegisterApiView(APIView):
    """
    Register a new user and return access + refresh tokens.
    """

    @extend_schema(
        request=AuthRegisterInputSerializer,
        responses={200: AuthRegisterOutputSerializer},
        tags=AUTH_TAG,
        summary="Register a new user",
        description="""
        Creates a new user account.

        **Flow:**
        - Validates unique username
        - Creates user in database
        - Hashes password
        - Returns JWT access + refresh tokens

        Use the returned `access_token` for authorized API requests.
        """,
    )
    def post(self, request):
        serializer = AuthRegisterInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        try:
            tokens = register_user_service(
                username=data["username"],
                password=data["password"],
                first_name=data.get("first_name", ""),
                last_name=data.get("last_name", ""),
            )

            return Response(
                AuthRegisterOutputSerializer(tokens).data,
                status=status.HTTP_200_OK,
            )

        except ValidationError:
            raise
        except Exception as e:
            logger.error(f"User registration failed for {data.get('username')}: {e}")
            return Response(
                {"detail": _("failed to register user. please try again.")},
                status=status.HTTP_400_BAD_REQUEST,
            )
