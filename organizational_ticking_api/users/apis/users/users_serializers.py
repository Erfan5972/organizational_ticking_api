from rest_framework import serializers

from organizational_ticking_api.users.models import BaseUser


class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseUser
        fields = ["username", "first_name", "last_name", "is_admin"]
