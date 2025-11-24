from django.db import models
from django.utils.translation import gettext_lazy as _

from django.contrib.auth import get_user_model

User = get_user_model()


class Ticket(models.Model):
    """
    Ticket model used for user support requests.

    Requirements:
    - Users can only see their own tickets.
    - Admin can see all tickets.
    - Users can edit/delete the ticket ONLY before first response.
    - Users cannot change the status (only Admin).
    - Supports filtering by status, priority, and text search.
    """

    class Priority(models.TextChoices):
        LOW = "low", _("Low")
        MEDIUM = "medium", _("Medium")
        HIGH = "high", _("High")

    class Status(models.TextChoices):
        OPEN = "open", _("Open")
        IN_PROGRESS = "in_progress", _("In Progress")
        CLOSED = "closed", _("Closed")

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="tickets",
        help_text=_("User who created the ticket."),
    )

    title = models.CharField(
        max_length=255,
        help_text=_("Short title describing the issue."),
    )

    description = models.TextField(
        help_text=_("Detailed explanation of the problem."),
    )

    priority = models.CharField(
        max_length=10,
        choices=Priority.choices,
        default=Priority.MEDIUM,
        db_index=True,
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.OPEN,
        db_index=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Ticket #{self.id} - {self.title}"
