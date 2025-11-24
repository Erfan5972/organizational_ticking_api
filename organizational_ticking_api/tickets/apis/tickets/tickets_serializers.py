from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from organizational_ticking_api.api.serializers import PaginatedSwaggerSerializer
from organizational_ticking_api.tickets.models import Ticket


class TicketParamSerializer(serializers.Serializer):
    """
    Serializer used for filtering the list of tickets.

    Supported query parameters:
    - status: Filter tickets by their current status.
    - priority: Filter tickets by priority level.
    - search: Search in title and description fields (case-insensitive).
    """

    status = serializers.CharField(
        required=False,
        help_text=_(
            "Filter tickets by status. Allowed values: open, in_progress, closed."
        ),
    )

    priority = serializers.CharField(
        required=False,
        help_text=_("Filter tickets by priority. Allowed values: low, medium, high."),
    )

    search = serializers.CharField(
        required=False,
        help_text=_("Search text across title and description fields."),
    )

    def validate_status(self, value):
        allowed = {"open", "in_progress", "closed"}
        if value not in allowed:
            raise serializers.ValidationError(
                _("Invalid status. Valid choices are: open, in_progress, closed")
            )


class TicketListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = [
            "id",
            "title",
            "priority",
            "status",
            "created_at",
        ]


class TicketListPaginatedSerializer(PaginatedSwaggerSerializer):
    results = serializers.ListField(child=TicketListSerializer())


class TicketCreateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    description = serializers.CharField()
    priority = serializers.ChoiceField(choices=Ticket.Priority.choices)
