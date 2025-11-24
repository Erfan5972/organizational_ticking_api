from rest_framework import serializers


class AuthRegisterInputSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=150, help_text="Unique username for login."
    )
    password = serializers.CharField(write_only=True, help_text="Account password.")
    first_name = serializers.CharField(
        required=False, allow_blank=True, help_text="Optional first name."
    )
    last_name = serializers.CharField(
        required=False, allow_blank=True, help_text="Optional last name."
    )


class AuthRegisterOutputSerializer(serializers.Serializer):
    access_token = serializers.CharField()
    refresh_token = serializers.CharField()
