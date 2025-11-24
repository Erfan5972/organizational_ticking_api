import logging
from drf_spectacular.utils import extend_schema, OpenApiResponse

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from organizational_ticking_api.api.mixins import ApiAuthMixin
from organizational_ticking_api.tickets.apis.tickets.id.tickets_id_serializers import (
    TicketDetailSerializer,
    TicketUpdateSerializer,
)
from organizational_ticking_api.tickets.constants import TICKET_TAGS
from organizational_ticking_api.tickets.selectors.tickets_selectors import (
    get_ticket_by_id,
)
from organizational_ticking_api.tickets.services.tickets_services import (
    partial_update_ticket_service,
    update_ticket_service,
    delete_ticket_by_id_service,
)

logger = logging.getLogger(__name__)


@extend_schema(
    tags=TICKET_TAGS,
    summary="Retrieve, update, or delete a ticket",
    description=(
        "This endpoint allows authenticated users to retrieve a ticket, "
        "update it (PUT/PATCH), or delete it. \n\n"
        "**Rules:**\n"
        "- Users can only edit/delete **their own tickets**.\n"
        "- Users can edit/delete only **before first response**.\n"
        "- Admins can update, but **cannot delete** tickets.\n"
    ),
)
class TicketRetrieveUpdateDeleteApiView(ApiAuthMixin, APIView):
    """
    API View for:
    - GET: Retrieve ticket details including responses
    - PUT: Fully update a ticket
    - PATCH: Partially update a ticket
    - DELETE: Delete a ticket based on business rules

    Business Rules:
    ---------------
    ✓ User can only manage **own tickets**
    ✓ User can update/delete only if **no responses** exist
    ✓ Admin can update any ticket
    ✘ Admin CANNOT delete tickets
    """

    # ---------------------------------------------------------------
    # GET /tickets/<id>/
    # ---------------------------------------------------------------
    @extend_schema(
        summary="Retrieve ticket details",
        responses={200: TicketDetailSerializer},
    )
    def get(self, request, ticket_id: int):
        """
        Retrieve a single ticket by ID.
        Returns ticket details with responses nested inside.
        """
        ticket = get_ticket_by_id(ticket_id=ticket_id)
        return Response(
            data=TicketDetailSerializer(ticket).data,
            status=status.HTTP_200_OK,
        )

    # ---------------------------------------------------------------
    # PUT /tickets/<id>/
    # ---------------------------------------------------------------
    @extend_schema(
        summary="Fully update a ticket (PUT)",
        request=TicketUpdateSerializer,
        responses={200: TicketDetailSerializer},
    )
    def put(self, request, ticket_id: int):
        """
        Fully update a ticket.
        Unlike PATCH, all fields must be present in the request.
        """
        serializer = TicketUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        updated_ticket = update_ticket_service(
            user=request.user,
            ticket_id=ticket_id,
            data=serializer.validated_data,
        )

        return Response(
            data=TicketDetailSerializer(updated_ticket).data,
            status=status.HTTP_200_OK,
        )

    # ---------------------------------------------------------------
    # PATCH /tickets/<id>/
    # ---------------------------------------------------------------
    @extend_schema(
        summary="Partially update a ticket (PATCH)",
        request=TicketUpdateSerializer,
        responses={200: TicketDetailSerializer},
    )
    def patch(self, request, ticket_id: int):
        """
        Partially update a ticket.
        Only supplied fields will be updated.
        """
        serializer = TicketUpdateSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        updated_ticket = partial_update_ticket_service(
            user=request.user,
            ticket_id=ticket_id,
            data=serializer.validated_data,
        )

        return Response(
            data=TicketDetailSerializer(updated_ticket).data,
            status=status.HTTP_200_OK,
        )

    # ---------------------------------------------------------------
    # DELETE /tickets/<id>/
    # ---------------------------------------------------------------
    @extend_schema(
        summary="Delete a ticket",
        description=(
            "**User:** Can delete only own ticket and only if it has **no responses**.\n"
            "**Admin:** Cannot delete tickets."
        ),
        responses={
            204: OpenApiResponse(description="Ticket successfully deleted"),
            403: OpenApiResponse(description="Forbidden"),
        },
    )
    def delete(self, request, ticket_id: int):
        """
        Delete a ticket.

        Rules:
        - User may delete only:
            • their own ticket
            • when the ticket has no responses
        - Admin cannot delete any ticket
        """
        delete_ticket_by_id_service(
            ticket_id=ticket_id,
            user=request.user,
        )

        return Response(status=status.HTTP_204_NO_CONTENT)
