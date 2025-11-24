from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from organizational_ticking_api.tickets.apis.tickets.id.responses.tickets_id_responses_serializers import (
    TicketResponseSerializer,
)
from organizational_ticking_api.tickets.models import Ticket
from organizational_ticking_api.users.apis.users.users_serializers import (
    SimpleUserSerializer,
)


class TicketDetailSerializer(serializers.ModelSerializer):
    responses = serializers.SerializerMethodField()
    user = SimpleUserSerializer()

    class Meta:
        model = Ticket
        fields = (
            "id",
            "title",
            "description",
            "priority",
            "status",
            "created_at",
            "updated_at",
            "user",
            "responses",
        )

    def get_responses(self, obj):
        responses = obj.responses.select_related("user").order_by("created_at")
        return TicketResponseSerializer(responses, many=True).data


class TicketUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer used for updating ticket information.

    Supports:
    - Full update (PUT)
    - Partial update (PATCH)

    Notes:
    - The `status` field is intentionally excluded because only Admin
      is allowed to update ticket status (via a special endpoint).
    """

    class Meta:
        model = Ticket
        fields = [
            "title",
            "description",
            "priority",
        ]
        extra_kwargs = {
            "title": {
                "required": False,
                "help_text": _("Short title describing the issue."),
            },
            "description": {
                "required": False,
                "help_text": _("Detailed explanation of the problem."),
            },
            "priority": {
                "required": False,
                "help_text": _("Priority of the ticket (low, medium, high)."),
            },
        }

    def validate_priority(self, value):
        if value not in Ticket.Priority.values:
            raise serializers.ValidationError(
                _("Invalid priority. Allowed values: low, medium, high.")
            )
        return value
