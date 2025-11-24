from django.core.exceptions import PermissionDenied
from django.contrib.auth import get_user_model

from organizational_ticking_api.tickets.models import Ticket
from organizational_ticking_api.tickets.selectors.tickets_selectors import (
    get_ticket_by_id,
)

User = get_user_model()


def create_ticket_service(
    *, user: User, title: str, description: str, priority: str
) -> Ticket:
    """
    Create a new ticket.

    Args:
        user (User): The user creating the ticket.
        title (str): Short title of the issue.
        description (str): Detailed description of the issue.
        priority (str): Priority level (low, medium, high).

    Returns:
        Ticket: Newly created Ticket instance.
    """
    return Ticket.objects.create(
        user=user,
        title=title,
        description=description,
        priority=priority,
    )


def update_ticket_service(*, user: User, ticket_id: int, data: dict) -> Ticket:
    """
    Fully update (PUT) a ticket.

    Rules:
    - User can update ONLY their own ticket.
    - User can update ONLY when the ticket has NO responses.
    - Admin can update any ticket.
    - Status CANNOT be updated here (admin-only endpoint).

    Raises:
        PermissionDenied: If update action is not allowed.
        Ticket.DoesNotExist: If ticket does not exist.

    Returns:
        Ticket: Updated ticket instance.
    """

    ticket = get_ticket_by_id(ticket_id=ticket_id)

    # Permission: user can edit only their own ticket
    if not user.is_admin and ticket.user_id != user.id:
        raise PermissionDenied("You do not have permission to edit this ticket.")

    # Rule: cannot edit after first response
    if ticket.responses.exists():
        raise PermissionDenied("You cannot edit a ticket after the first response.")

    # Prevent status updates here
    if "status" in data:
        raise PermissionDenied("Ticket status can only be changed by an admin.")

    # Apply full update (PUT)
    ticket.title = data["title"]
    ticket.description = data["description"]
    ticket.priority = data["priority"]
    ticket.save()

    return ticket


def partial_update_ticket_service(*, user: User, ticket_id: int, data: dict) -> Ticket:
    """
    Partially update (PATCH) a ticket.

    Rules:
    - User can update ONLY their own ticket.
    - User can update ONLY when the ticket has NO responses.
    - Admin can update any ticket.
    - Status cannot be updated here.

    Raises:
        PermissionDenied: If update not allowed.
        Ticket.DoesNotExist: If ticket not found.

    Returns:
        Ticket: Updated ticket instance.
    """

    ticket = get_ticket_by_id(ticket_id=ticket_id)

    # Permission: user can edit only their own ticket
    if not user.is_admin and ticket.user_id != user.id:
        raise PermissionDenied("You cannot edit this ticket.")

    # Rule: cannot edit after first response
    if ticket.responses.exists():
        raise PermissionDenied("You cannot edit a ticket after the first response.")

    # Prevent status updates here
    if "status" in data:
        raise PermissionDenied("Only admins can change ticket status.")

    # Apply partial update
    for field, value in data.items():
        setattr(ticket, field, value)

    ticket.save()
    return ticket


def delete_ticket_by_id_service(*, ticket_id: int, user: User) -> bool:
    """
    Delete a ticket by ID.

    Rules:
    - User (normal user):
        • Can delete ONLY their own ticket.
        • Can delete ONLY if the ticket has NO responses.
    - Admin:
        • Admin CANNOT delete tickets (project rule).

    Args:
        ticket_id (int): ID of the ticket to delete.
        user (User): User requesting deletion.

    Returns:
        bool: True if deletion was successful.

    Raises:
        PermissionDenied: If the user is not allowed to delete the ticket.
        Ticket.DoesNotExist: If the ticket does not exist.
    """

    ticket = get_ticket_by_id(ticket_id=ticket_id)

    # Admin cannot delete
    if user.is_admin:
        raise PermissionDenied("Admins are not allowed to delete tickets.")

    # Normal user: must own the ticket
    if ticket.user_id != user.id:
        raise PermissionDenied("You do not have permission to delete this ticket.")

    # Cannot delete a ticket that has any responses
    if ticket.responses.exists():
        raise PermissionDenied("You cannot delete a ticket that already has responses.")

    ticket.delete()
    return True


def update_ticket_status_service(*, user: User, ticket_id: int, status: str) -> Ticket:
    """
    Update the status of a ticket.

    Rules:
    - Only admins can update the ticket status.
    - Raises PermissionDenied if user is not admin.
    - Raises Ticket.DoesNotExist if ticket is not found.
    """
    ticket = get_ticket_by_id(ticket_id=ticket_id)

    if not user.is_admin:
        raise PermissionDenied("Only admins can update ticket status.")

    ticket.status = status
    ticket.save()
    return ticket
