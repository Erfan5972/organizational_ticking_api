from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

from organizational_ticking_api.tickets.models import Ticket

User = get_user_model()


class TicketResponse(models.Model):
    """
    A response to a ticket.

    Requirements:
    - User can add responses (before first Admin action depending on rules).
    - Admin can always respond.
    - Messages belong to a ticket.
    """

    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        related_name="responses",
        help_text=_("The ticket this response belongs to."),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="ticket_responses",
        help_text=_("User who wrote the response."),
    )

    message = models.TextField(
        help_text=_("Message body of the response."),
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Response #{self.id} to Ticket #{self.ticket_id}"
