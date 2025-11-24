from rest_framework import serializers

from organizational_ticking_api.api.serializers import PaginatedSwaggerSerializer
from organizational_ticking_api.tickets.models import TicketResponse
from organizational_ticking_api.users.apis.users.users_serializers import (
    SimpleUserSerializer,
)


class TicketResponseSerializer(serializers.ModelSerializer):
    user = SimpleUserSerializer()

    class Meta:
        model = TicketResponse
        fields = ("id", "ticket_id", "user", "message", "created_at")


class TicketResponseCreateSerializer(serializers.Serializer):
    ticket_id = serializers.IntegerField(help_text="ID of the ticket to respond to.")
    message = serializers.CharField(help_text="The message body of the response.")


class TicketListPaginatedSerializer(PaginatedSwaggerSerializer):
    results = serializers.ListField(child=TicketResponseSerializer())
