from drf_spectacular.utils import extend_schema

from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from organizational_ticking_api.users.apis.auth.refresh_token.users_auth_refresh_serializers import (
    RefreshTokenInputSerializer,
    RefreshTokenOutputSerializer,
)
from organizational_ticking_api.users.constants import AUTH_TAG
from organizational_ticking_api.users.services.auth_services import (
    refresh_user_token_service,
)


class RefreshTokenApiView(APIView):
    @extend_schema(
        request=RefreshTokenInputSerializer,
        responses={"200": RefreshTokenOutputSerializer},
        tags=AUTH_TAG,
        summary="Refresh user token",
        description=(
            "Refreshes a user's authentication tokens by validating their refresh token "
            "and issuing new access and refresh tokens.\n\n This endpoint is used when the "
            "current access token has expired but the refresh token is still valid. "
            "\n\nThe new tokens maintain the user's authenticated session without requiring re-login."
        ),
    )
    def post(self, request: Request):
        """
        Gets user's refresh token and return new access token and refresh token

        Returns:
            dict: The refreshed tokens.

        Raises:
            AuthenticationFailed: If the credentials are invalid.
        """
        refresh_token_serializer = RefreshTokenInputSerializer(data=request.data)
        refresh_token_serializer.is_valid(raise_exception=True)
        refresh_token = refresh_token_serializer.validated_data.get("refresh_token")
        if not refresh_token:
            return Response(
                {
                    "detail": _(
                        "invalid refresh token. please check your refresh token."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        token = refresh_user_token_service(refresh_token)
        output_serializer = RefreshTokenOutputSerializer(token)
        return Response(output_serializer.data, status=status.HTTP_200_OK)
