from rest_framework.exceptions import PermissionDenied
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from organizational_ticking_api.tickets.models import TicketResponse

User = get_user_model()


def get_ticket_response_by_id(response_id: int) -> TicketResponse:
    """
    Fetch a TicketResponse by ID.

    Raises:
        TicketResponse.DoesNotExist
    """
    return TicketResponse.objects.select_related("ticket", "user").get(id=response_id)


def list_ticket_responses(ticket_id: int, user: User):
    """
    List all responses for a given ticket, ordered by creation date.
    """
    if not user.is_admin:
        raise PermissionDenied(_("Only admin can perform this action"))
    return (
        TicketResponse.objects.filter(ticket_id=ticket_id)
        .select_related("user")
        .order_by("created_at")
    )
