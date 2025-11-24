import logging
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _

from organizational_ticking_api.api.mixins import ApiAuthMixin
from organizational_ticking_api.api.pagination import (
    PageNumberPagination,
    get_paginated_response,
)
from organizational_ticking_api.tickets.apis.tickets.tickets_serializers import (
    TicketParamSerializer,
    TicketListSerializer,
    TicketCreateSerializer,
    TicketListPaginatedSerializer,
)
from organizational_ticking_api.tickets.constants import TICKET_TAGS
from organizational_ticking_api.tickets.selectors.tickets_selectors import (
    list_tickets_selector,
)
from organizational_ticking_api.tickets.services.tickets_services import (
    create_ticket_service,
)
from organizational_ticking_api.api.serializers import PaginationParametersSerializer

logger = logging.getLogger(__name__)


@extend_schema(
    tags=TICKET_TAGS,
    description=(
        "List and create tickets.\n\n"
        "GET: Returns paginated tickets.\n"
        "POST: Create a new ticket."
    ),
)
class TicketListCreateApiView(ApiAuthMixin, APIView):
    # ----------------------
    # GET /tickets/
    # ----------------------
    @extend_schema(
        summary="List tickets with pagination and filters",
        parameters=[PaginationParametersSerializer, TicketParamSerializer],
        responses={200: TicketListPaginatedSerializer},
    )
    def get(self, request):
        """
        List tickets with optional filters and pagination.
        """
        param_serializer = TicketParamSerializer(data=request.query_params)
        param_serializer.is_valid(raise_exception=True)

        qs = list_tickets_selector(
            user=request.user,
            is_admin=getattr(request.user, "is_admin", False),
            priority=param_serializer.validated_data.get("priority"),
            status=param_serializer.validated_data.get("status"),
            search=param_serializer.validated_data.get("search"),
        )

        return get_paginated_response(
            request=request,
            pagination_class=PageNumberPagination,
            queryset=qs,
            serializer_class=TicketListSerializer,
            view=self,
        )

    # ----------------------
    # POST /tickets/
    # ----------------------
    @extend_schema(
        summary="Create a new ticket",
        request=TicketCreateSerializer,
        responses={
            201: TicketListSerializer,
            400: OpenApiResponse(description="Validation or creation error"),
        },
    )
    def post(self, request):
        """
        Create a new ticket.
        """
        serializer = TicketCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            ticket = create_ticket_service(
                user=request.user,
                title=serializer.validated_data["title"],
                description=serializer.validated_data["description"],
                priority=serializer.validated_data["priority"],
            )
            out = TicketListSerializer(ticket)
            return Response(out.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(f"Failed to create ticket for user {request.user.id}: {e}")
            return Response(
                {"detail": _("failed to create ticket.")},
                status=status.HTTP_400_BAD_REQUEST,
            )
