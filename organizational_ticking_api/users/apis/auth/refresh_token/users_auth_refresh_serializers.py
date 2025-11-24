from rest_framework import serializers


class RefreshTokenInputSerializer(serializers.Serializer):
    """
    Serializer for refresh token API request.
    """

    refresh_token = serializers.CharField(
        help_text="JWT refresh token to obtain new access tokens"
    )


class RefreshTokenOutputSerializer(serializers.Serializer):
    """
    Serializer for refresh token API response.
    """

    refresh_token = serializers.CharField(
        help_text="JWT refresh token to obtain new access tokens"
    )
    access_token = serializers.CharField(
        help_text="JWT access token for API authentication"
    )
