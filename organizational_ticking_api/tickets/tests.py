import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from organizational_ticking_api.users.models import BaseUser
from organizational_ticking_api.tickets.models import Ticket, TicketResponse

pytestmark = pytest.mark.django_db


# ----------------------------
# Fixtures
# ----------------------------


@pytest.fixture
def user():
    return BaseUser.objects.create_user(username="testuser", password="password123")


@pytest.fixture
def admin():
    return BaseUser.objects.create_user(
        username="adminuser", password="adminpass", is_admin=True
    )


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def ticket(user):
    return Ticket.objects.create(
        user=user,
        title="Test Ticket",
        description="This is a test ticket",
        priority="medium",
    )


@pytest.fixture
def ticket_with_response(user, admin):
    t = Ticket.objects.create(
        user=user,
        title="Ticket with Response",
        description="Ticket has a response",
        priority="high",
    )
    TicketResponse.objects.create(ticket=t, user=admin, message="Admin response")
    return t


# ----------------------------
# Ticket APIs
# ----------------------------


def test_create_ticket(api_client, user):
    api_client.force_authenticate(user=user)
    url = reverse("api:tickets:list_create_tickets")
    data = {"title": "New Ticket", "description": "Ticket desc", "priority": "high"}
    resp = api_client.post(url, data, format="json")
    assert resp.status_code == status.HTTP_201_CREATED
    assert resp.data["title"] == "New Ticket"


def test_update_ticket_before_response(api_client, user, ticket):
    api_client.force_authenticate(user=user)
    url = reverse(
        "api:tickets:get_update_delete_tickets", kwargs={"ticket_id": ticket.id}
    )
    data = {"title": "Updated Title", "description": "Updated desc", "priority": "low"}
    resp = api_client.put(url, data, format="json")
    assert resp.status_code == status.HTTP_200_OK
    ticket.refresh_from_db()
    assert ticket.title == "Updated Title"


def test_cannot_update_ticket_after_response(api_client, user, ticket_with_response):
    api_client.force_authenticate(user=user)
    url = reverse(
        "api:tickets:get_update_delete_tickets",
        kwargs={"ticket_id": ticket_with_response.id},
    )
    data = {"title": "Try Update", "description": "Desc", "priority": "low"}
    resp = api_client.put(url, data, format="json")
    assert resp.status_code == status.HTTP_403_FORBIDDEN


def test_admin_can_change_ticket_status(api_client, admin, ticket):
    api_client.force_authenticate(user=admin)
    url = reverse("api:tickets:update_ticket_status", kwargs={"ticket_id": ticket.id})
    data = {"status": "in_progress"}
    resp = api_client.patch(url, data, format="json")
    assert resp.status_code == status.HTTP_200_OK
    ticket.refresh_from_db()
    assert ticket.status == "in_progress"
