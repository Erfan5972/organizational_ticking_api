from rest_framework import serializers


class AuthLogoutInputSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(
        help_text="Refresh token to be blacklisted on logout."
    )


class AuthLogoutOutputSerializer(serializers.Serializer):
    message = serializers.CharField()
