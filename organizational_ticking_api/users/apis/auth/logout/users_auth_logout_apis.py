import logging
from drf_spectacular.utils import extend_schema

from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication


from organizational_ticking_api.users.apis.auth.logout.users_auth_logout_serializers import (
    AuthLogoutInputSerializer,
    AuthLogoutOutputSerializer,
)
from organizational_ticking_api.api.mixins import ApiAuthMixin
from organizational_ticking_api.users.constants import AUTH_TAG
from organizational_ticking_api.users.services.auth_services import (
    logout_user_service,
)

logger = logging.getLogger(__name__)


class LogoutApiView(ApiAuthMixin, APIView):
    """
    Logout user by blacklisting refresh token.
    """

    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    @extend_schema(
        request=AuthLogoutInputSerializer,
        responses={200: AuthLogoutOutputSerializer},
        tags=AUTH_TAG,
        summary="Logout user (Blacklist Refresh Token)",
        description="""
        Logs out the user by **blacklisting the refresh token**.

        After logout:
        - The refresh token becomes invalid permanently.
        - The access token expires naturally and cannot be refreshed anymore.

        **Usage:**
        Send the refresh_token obtained from login to this endpoint.
        """,
    )
    def post(self, request):
        serializer = AuthLogoutInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        refresh_token = serializer.validated_data["refresh_token"]

        try:
            logout_user_service(refresh_token=refresh_token)
            return Response(
                AuthLogoutOutputSerializer({"message": _("logout successful.")}).data,
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            logger.warning(
                f"Logout failed for refresh token: {refresh_token} - {str(e)}"
            )
            return Response(
                {"detail": _("invalid or expired token.")},
                status=status.HTTP_400_BAD_REQUEST,
            )
