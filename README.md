# Organizational Ticketing API

A **Django REST Framework (DRF)** project for managing user support tickets, built with **JWT authentication**, **role-based permissions**, and fully documented APIs using **drf-spectacular (OpenAPI/Swagger)**.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Code Structure](#code-structure)
3. [Models](#models)
    - [BaseUser](#baseuser)
    - [Ticket](#ticket)
    - [TicketResponse](#ticketresponse)
4. [API Endpoints](#api-endpoints)
    - [Authentication](#authentication)
    - [Tickets](#tickets)
    - [Ticket Responses](#ticket-responses)
5. [Permissions and Business Rules](#permissions-and-business-rules)
6. [Pagination and Filtering](#pagination-and-filtering)
7. [Example Requests](#example-requests)
8. [Swagger / OpenAPI Docs](#swagger--openapi-docs)

---

## Project Overview

This project allows users to create support tickets and communicate with the support/admin team through **ticket responses**.

Key features:

- JWT-based authentication (`login`, `logout`, `refresh`)
- Users can only see/edit their tickets (before admin response)
- Admins can manage all tickets and responses
- Filtering by `status`, `priority`, and text search
- Pagination support

## Models

### BaseUser

Custom user model with the following fields:

| Field       | Description |
| ----------- | ----------- |
| `username`  | Unique identifier for login |
| `first_name`| Optional first name |
| `last_name` | Optional last name |
| `is_active` | Boolean: active user |
| `is_staff`  | Boolean: staff/admin user |
| `date_joined` | Timestamp of account creation |
| `full_name` | Property returning `first_name last_name` |

---

### Ticket

Represents a support ticket.

| Field       | Description |
| ----------- | ----------- |
| `user`      | Creator of the ticket |
| `title`     | Short title of the issue |
| `description` | Full description |
| `priority`  | `low`, `medium`, `high` |
| `status`    | `open`, `in_progress`, `closed` |
| `created_at` | Timestamp |
| `updated_at` | Timestamp |

---

### TicketResponse

Represents a response to a ticket.

| Field       | Description |
| ----------- | ----------- |
| `ticket`    | Foreign key to Ticket |
| `user`      | Creator of the response (user/admin) |
| `message`   | Response message |
| `created_at`| Timestamp |

---

## API Endpoints

### Authentication

| Endpoint | Method | Description |
| -------- | ------ | ----------- |
| `/auth/login/` | POST | Login and get JWT tokens |
| `/auth/logout/` | POST | Logout (blacklist refresh token) |
| `/auth/refresh/` | POST | Refresh access token |

---

### Tickets

| Endpoint | Method | Description |
| -------- | ------ | ----------- |
| `/tickets/` | GET | List tickets (filterable & paginated) |
| `/tickets/` | POST | Create new ticket |
| `/tickets/<id>/` | GET | Get ticket details (with responses) |
| `/tickets/<id>/` | PUT | Full update ticket (before first response only for users) |
| `/tickets/<id>/` | PATCH | Partial update ticket |
| `/tickets/<id>/` | DELETE | Delete ticket (only if no responses) |
| `/tickets/<id>/status/` | PATCH | Admin-only: change ticket status |

---

### Ticket Responses

| Endpoint | Method | Description |
| -------- | ------ | ----------- |
| `/tickets/<id>/responses/` | GET | List responses for a ticket |
| `/tickets/<id>/responses/` | POST | Add a response (admin or user based on rules) |

---

## Permissions and Business Rules

- **User**
  - Can see only own tickets
  - Can create tickets
  - Can edit/delete tickets only **before first response**
  - Cannot change status (admin-only)
- **Admin**
  - Can see all tickets
  - Can respond to any ticket
  - Can update ticket status
  - Cannot delete tickets
- **Responses**
  - Users can respond only before first admin response
  - Admin can respond anytime

---

## Pagination and Filtering

- **Pagination parameters**
  - `p` → page number
  - `page_size` → number of objects per page
  - `all` → show all objects (optional)

- **Filtering**
  - `status` → filter by ticket status (`open`, `in_progress`, `closed`)
  - `priority` → filter by ticket priority (`low`, `medium`, `high`)
  - `search` → search in `title` and `description`

---

## Example Requests

### Create Ticket

```http
POST /tickets/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "title": "Cannot login",
  "description": "I am unable to login to my account",
  "priority": "high"
}
Update Ticket Status (Admin Only)
PATCH /tickets/1/status/
Authorization: Bearer <admin_access_token>
Content-Type: application/json

{
  "status": "in_progress"
}
List Tickets with Filters
GET /tickets/?status=open&priority=high&search=login&p=1&page_size=10
Authorization: Bearer <access_token>
POST /tickets/1/responses/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "message": "We are looking into this issue."
}
