# tickets/apis/tickets/status/tickets_status_api.py
import logging
from drf_spectacular.utils import extend_schema
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from organizational_ticking_api.api.mixins import ApiAuthMixin
from organizational_ticking_api.tickets.apis.tickets.id.status.tickets_id_status_serializers import (
    TicketStatusUpdateSerializer,
)
from organizational_ticking_api.tickets.services.tickets_services import (
    update_ticket_status_service,
)


logger = logging.getLogger(__name__)


class TicketStatusUpdateApiView(ApiAuthMixin, APIView):
    """
    Admin endpoint to update the status of a ticket.
    """

    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=TicketStatusUpdateSerializer,
        responses={200: TicketStatusUpdateSerializer},
        tags=["Tickets"],
        summary="Update ticket status",
        description="""
        Allows admin users to change the status of a ticket.

        **Rules:**
        - Only admin users can update the status.
        - Status can be one of: `open`, `in_progress`, `closed`.
        """,
    )
    def patch(self, request, ticket_id: int):
        serializer = TicketStatusUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        status_value = serializer.validated_data["status"]

        try:
            ticket = update_ticket_status_service(
                user=request.user, ticket_id=ticket_id, status=status_value
            )
            return Response(
                {"id": ticket.id, "status": ticket.status}, status=status.HTTP_200_OK
            )
        except Exception as e:
            logger.error(f"Failed to update status for ticket {ticket_id}: {e}")
            return Response(
                {"detail": _("Failed to update ticket status.")},
                status=status.HTTP_400_BAD_REQUEST,
            )
