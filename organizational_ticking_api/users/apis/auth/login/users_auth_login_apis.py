import logging
from drf_spectacular.utils import extend_schema

from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from organizational_ticking_api.users.apis.auth.login.users_auth_login_serializers import (
    AuthLoginInputSerializer,
    AuthLoginOutputSerializer,
)
from organizational_ticking_api.users.constants import AUTH_TAG
from organizational_ticking_api.users.services.auth_services import auth_login_service

logger = logging.getLogger(__name__)


class LoginApiView(APIView):
    """
    login user with username and password and captcha
    return refresh token and access token
    """

    @extend_schema(
        request=AuthLoginInputSerializer,
        responses={200: AuthLoginOutputSerializer},
        tags=AUTH_TAG,
        summary="Authenticate user and obtain JWT tokens",
        description="""Authenticate a user by validating their username and password credentials.
        This endpoint performs user authentication and upon successful validation, returns JWT tokens
        for secure API access. The response includes both an access token for immediate API calls
        and a refresh token for obtaining new access tokens when they expire.\n
        \n**Authentication Flow:**\n
        - Validates provided username and password against stored credentials
        - Generates secure JWT tokens upon successful authentication
        - Returns tokens for subsequent API authorization
        \n**Usage:**\n
        \nUse the returned access_token in the Authorization header for authenticated API requests.
        Use the refresh_token to obtain new access tokens when they expire.""",
    )
    def post(self, request):
        """
        Authenticates a user using the provided username and password.

        This endpoint receives a POST request with user credentials, validates them,
        and attempts to authenticate the user. If authentication is successful,
        it returns a response containing a refresh token and an access token.
        If authentication fails, it returns an error message with a 401 status code.

        Args:
            request (Request): The HTTP request object containing user credentials in the body.
                Expected fields:
                    - username (str): The user's username.
                    - password (str): The user's password.

        Returns:
            Response: On success, returns a 200 OK response with the following data:
                - access_token (str): JWT access token for authenticated requests.
                - refresh_token (str): JWT refresh token for obtaining new access tokens.
            On failure, returns a 401 Unauthorized response with an error message.

        Raises:
            ValidationError: If the input data is invalid (handled by serializer).
            Exception: For any authentication failure or unexpected error (returns 401).
        """
        login_serializer = AuthLoginInputSerializer(data=request.data)
        login_serializer.is_valid(raise_exception=True)

        try:
            jwt_token = auth_login_service(
                username=login_serializer.validated_data.get("username"),
                password=login_serializer.validated_data.get("password"),
            )
            return Response(
                AuthLoginOutputSerializer(jwt_token).data, status.HTTP_200_OK
            )
        except ValidationError as e:
            raise e
        except Exception as e:
            logger.warning(
                f"Failed login attempt for username: {login_serializer.validated_data.get('username')} - {str(e)}"
            )
            return Response(
                {
                    "detail": _(
                        "invalid credentials. please check your username and password."
                    )
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )
