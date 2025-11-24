from django.core.exceptions import PermissionDenied
from django.contrib.auth import get_user_model
from organizational_ticking_api.tickets.models import TicketResponse
from organizational_ticking_api.tickets.selectors.tickets_selectors import (
    get_ticket_by_id,
)

User = get_user_model()


def create_ticket_response_service(
    *, user: User, ticket_id: int, message: str
) -> TicketResponse:
    """
    Create a new response to a ticket.

    Rules:
    - Admin can respond anytime.
    - Normal users can respond only before the first admin response.
    - Raises PermissionDenied if user cannot respond.
    """
    ticket = get_ticket_by_id(ticket_id=ticket_id)

    # Admin can respond anytime
    if getattr(user, "is_admin", False):
        pass
    else:
        # Check if ticket already has an admin response
        if ticket.responses.filter(user__is_admin=True).exists():
            raise PermissionDenied("Cannot respond after an admin response.")
    return TicketResponse.objects.create(ticket=ticket, user=user, message=message)
