from django.urls import path

from organizational_ticking_api.tickets.apis import (
    TicketListCreateApiView,
    TicketRetrieveUpdateDeleteApiView,
    TicketResponseListCreateApiView,
    TicketStatusUpdateApiView,
)

app_name = "tickets"

urlpatterns = [
    # List all tickets or create a new ticket
    path("", TicketListCreateApiView.as_view(), name="list_create_tickets"),
    # Retrieve, update, or delete a specific ticket
    path(
        "<int:ticket_id>/",
        TicketRetrieveUpdateDeleteApiView.as_view(),
        name="get_update_delete_tickets",
    ),
    # List or create responses for a specific ticket
    path(
        "<int:ticket_id>/responses/",
        TicketResponseListCreateApiView.as_view(),
        name="list_create_ticket_responses",
    ),
    # Update status of a specific ticket (admin only)
    path(
        "<int:ticket_id>/status/",
        TicketStatusUpdateApiView.as_view(),
        name="update_ticket_status",
    ),
]
