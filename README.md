# Expense Claim API

A small backend API built with FastAPI, PostgreSQL, JWT authentication, and Docker.

This project allows employees to submit expense claims, managers to review claims from their direct reports, and admins to manage users and access all claims. The main goal of the project is to demonstrate correct authentication, authorization, and role-based access control.

## What this project contains

This project includes:

- A FastAPI backend
- PostgreSQL database
- JWT-based authentication
- Role-based access control for `EMPLOYEE`, `MANAGER`, and `ADMIN`
- Seeded users and sample claims
- Docker setup for local development
- Basic automated tests with `pytest`

## Features

- User login with JWT token
- Employee registration
- Profile endpoint for the logged-in user
- Expense claim creation
- Claim listing based on role permissions
- Claim status update by manager or admin
- User deletion by admin
- Seed data created automatically on first startup
- Login rate limiting

## Roles and permissions

### EMPLOYEE
- Can register
- Can log in
- Can view their own profile
- Can create claims
- Can view only their own claims

### MANAGER
- Can log in
- Can view their own profile
- Can view their own claims
- Can view claims of employees whose `manager_id` points to them
- Can approve or reject claims
- Cannot approve or reject their own claim

### ADMIN
- Can log in
- Can view their own profile
- Can view all claims
- Can approve or reject claims
- Can delete users

## API endpoints

- `POST /auth/register` - Register a new employee
- `POST /auth/login` - Log in and receive a JWT token
- `GET /me` - Get the current logged-in user
- `POST /claims` - Create a new claim as employee
- `GET /claims` - List claims based on role access
- `GET /claims/{id}` - Get one claim if allowed
- `PATCH /claims/{id}/status` - Approve or reject a claim as manager or admin
- `DELETE /users/{id}` - Delete a user as admin

## Seeded credentials

These users are created automatically on first startup:

| Email | Password | Role |
|-------|----------|------|
| admin@test.com | Admin@123 | ADMIN |
| manager@test.com | Manager@123 | MANAGER |
| emp1@test.com | Emp@123 | EMPLOYEE |
| emp2@test.com | Emp@123 | EMPLOYEE |
| emp3@test.com | Emp@123 | EMPLOYEE |

At least one `PENDING` claim is also created for each seeded employee.

## Tech stack

- FastAPI
- PostgreSQL
- SQLAlchemy
- JWT authentication
- bcrypt / password hashing
- Docker and Docker Compose
- Pytest

## How to run locally with Docker

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd expense-claim-api
```

### 2. Create the environment file

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

Then update the values in `.env` if needed.

### 3. Start the project

```bash
docker compose up --build
```

This starts both:
- the FastAPI application
- the PostgreSQL database

The API should be available at:

```text
http://localhost:8000
```

Swagger documentation should be available at:

```text
http://localhost:8000/docs
```

## How to stop and rebuild

To stop the containers and start again:

```bash
docker compose down
docker compose up --build
```

If you want a fresh reset including database data:

```bash
docker compose down --volumes
docker compose up --build --force-recreate
```

## How to run tests

```bash
pytest tests -v
```

## Important business rules

- An employee can only see their own claims.
- A manager can only see their own claims and the claims of their direct reports.
- An admin can see all claims.
- A manager cannot update the status of their own claim.
- Only `PENDING` claims can be changed to `APPROVED` or `REJECTED`.
- If a user tries to access a claim they are not allowed to see, the API returns `403`.

## Assumptions

Some parts of the task were intentionally left slightly open, so the following implementation decisions were made:

- `POST /auth/register` creates only `EMPLOYEE` users.
- `manager_id` is handled on the server side and is not trusted from client input.
- Seed data is created only on first startup if it does not already exist.
- Seeded employee claims are created with `PENDING` status.
- If a claim exists but the current user is not allowed to access it, the API returns `403` as required.
- Login responses use a generic error message so the API does not reveal whether the email or password was incorrect.
- Login rate limiting is currently implemented in memory for simplicity in this task.

## Known behavior

### Login rate limit behavior

The current login rate limiting behavior is:

- Failed attempts 1 to 5 return `401 Unauthorized`
- The response body is:

```json
{
  "detail": "Invalid email or password"
}
```

- The 6th failed attempt returns `429 Too Many Requests`
- The response body is:

```json
{
  "detail": "Too many failed login attempts. Please try again later."
}
```

- If the 7th attempt uses the correct password, login succeeds in the current implementation

This works for the task requirement, but in a production system it would be better to block further attempts for a cooldown period once the limit is reached.

## What I would do with more time

### 1. Protect admin deletion better
At the moment, an admin can delete themself. This creates a risk that the last remaining admin could be deleted, leaving the system with no admin user. A better implementation would:

- prevent the last admin from deleting themself
- prevent deletion of the seeded admin account

### 2. Improve login rate limiting
The current rate limiter uses in-memory storage. This means:

- it resets when the app restarts
- it works only per container
- it is not ideal for production use

For production, Redis or a database-backed rate limiter would be a better solution.

### 3. Make login blocking stricter after too many failures
Right now:

- first 5 failed attempts return `401`
- the 6th failed attempt returns `429`
- a correct 7th attempt can still succeed

A more secure production approach would temporarily block login attempts after the threshold is reached, even if the next password is correct. This would make brute-force protection stronger and more predictable.

### 4. Add more tests
More time would also be used to add additional tests for:

- admin deletion edge cases
- login rate limiting edge cases
- claim visibility checks
- seeded data behavior
- invalid status update attempts

### 5. Add migrations
Database migrations using Alembic would be better than relying only on table creation at startup.

### 6. Improve observability
Structured logging and better error monitoring would make the application easier to debug and maintain.

## Notes

This project was built with a focus on clear structure, correct authorization logic, and simple local setup with Docker.