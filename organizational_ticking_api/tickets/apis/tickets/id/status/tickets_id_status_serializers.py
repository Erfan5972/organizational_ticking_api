# tickets/apis/tickets/status/tickets_status_serializers.py
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _


class TicketStatusUpdateSerializer(serializers.Serializer):
    """
    Serializer for updating ticket status.
    """

    status = serializers.ChoiceField(
        choices=["open", "in_progress", "closed"],
        help_text=_("New status of the ticket. Only admins can update."),
    )
