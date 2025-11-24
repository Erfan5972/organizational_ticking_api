from rest_framework import serializers


class AuthLoginInputSerializer(serializers.Serializer):
    """
    Serializer for login API request.
    """

    username = serializers.CharField(
        help_text="A unique identifier used for user login. Must be unique across all users."
    )
    password = serializers.CharField(
        help_text=(
            "A secret string used to authenticate the user. Must be kept confidential and meet security requirements. "
            "Required for logging in and protecting the user account from unauthorized access."
        )
    )


class AuthLoginOutputSerializer(serializers.Serializer):
    """
    Serializer for login API response.
    """

    access_token = serializers.CharField(
        help_text="JWT access token for API authentication"
    )
    refresh_token = serializers.CharField(
        help_text="JWT refresh token to obtain new access tokens"
    )
