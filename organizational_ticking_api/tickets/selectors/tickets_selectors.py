from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import NotFound

from organizational_ticking_api.tickets.models import Ticket


def get_ticket_by_id(ticket_id: int) -> Ticket | None:
    """
    Return a single ticket by ID.
    """
    try:
        return Ticket.objects.get(id=ticket_id)
    except Ticket.DoesNotExist:
        return NotFound(_("Ticket with this id not found"))


def list_tickets_selector(
    *,
    user,
    is_admin: bool,
    status: str | None,
    priority: str | None,
    search: str | None,
):
    """
    Return a queryset of tickets based on filters and user.
    """
    qs = Ticket.objects.all()

    # User can only see their own tickets
    if not is_admin:
        qs = qs.filter(user=user)

    if status:
        qs = qs.filter(status=status)

    if priority:
        qs = qs.filter(priority=priority)

    if search:
        qs = qs.filter(Q(title__icontains=search) | Q(description__icontains=search))

    return qs.order_by("-created_at")
