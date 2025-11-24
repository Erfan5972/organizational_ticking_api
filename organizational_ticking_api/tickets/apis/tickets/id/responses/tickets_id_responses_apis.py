import logging
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from organizational_ticking_api.api.mixins import ApiAuthMixin
from organizational_ticking_api.api.pagination import (
    PageNumberPagination,
    get_paginated_response,
)
from organizational_ticking_api.tickets.apis.tickets.id.responses.tickets_id_responses_serializers import (
    TicketListPaginatedSerializer,
    TicketResponseCreateSerializer,
    TicketResponseSerializer,
)
from organizational_ticking_api.tickets.constants import TICKET_TAGS
from organizational_ticking_api.tickets.services.ticket_response_services import (
    create_ticket_response_service,
)
from organizational_ticking_api.tickets.selectors.ticket_response_selectors import (
    list_ticket_responses,
)

logger = logging.getLogger(__name__)


class TicketResponseListCreateApiView(ApiAuthMixin, APIView):
    """
    List or create responses for a ticket.
    """

    @extend_schema(
        summary="List all responses of a ticket",
        description="Returns all responses for a given ticket, ordered by creation date.",
        responses={200: TicketListPaginatedSerializer()},
        tags=TICKET_TAGS,
    )
    def get(self, request, ticket_id: int):
        responses_qs = list_ticket_responses(ticket_id=ticket_id, user=request.user)
        return get_paginated_response(
            request=request,
            pagination_class=PageNumberPagination,
            queryset=responses_qs,
            serializer_class=TicketResponseSerializer,
            view=self,
        )

    @extend_schema(
        summary="Create a response for a ticket",
        request=TicketResponseCreateSerializer,
        responses={201: TicketResponseSerializer},
        tags=TICKET_TAGS,
        description="Create a new response. Admins can respond anytime; normal users can respond only before first admin response.",
    )
    def post(self, request, ticket_id: int):
        serializer = TicketResponseCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            response = create_ticket_response_service(
                user=request.user,
                ticket_id=ticket_id,
                message=serializer.validated_data.get("message"),
            )
            out_serializer = TicketResponseSerializer(response)
            return Response(out_serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(f"Failed to create response for ticket {ticket_id}: {e}")
            return Response(
                {"detail": "Failed to create ticket response."},
                status=status.HTTP_400_BAD_REQUEST,
            )
