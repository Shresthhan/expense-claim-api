import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


def login_and_get_token(client: TestClient, email: str, password: str) -> str:
    response = client.post(
        "/auth/login",
        json={
            "email": email,
            "password": password,
        },
    )
    assert response.status_code == 200
    return response.json()["access_token"]


@pytest.fixture
def admin_token(client):
    return login_and_get_token(client, "admin@test.com", "Admin@123")


@pytest.fixture
def manager_token(client):
    return login_and_get_token(client, "manager@test.com", "Manager@123")


@pytest.fixture
def emp1_token(client):
    return login_and_get_token(client, "emp1@test.com", "Emp@123")


@pytest.fixture
def emp2_token(client):
    return login_and_get_token(client, "emp2@test.com", "Emp@123")


@pytest.fixture
def emp3_token(client):
    return login_and_get_token(client, "emp3@test.com", "Emp@123")


@pytest.fixture
def admin_headers(admin_token):
    return {"Authorization": f"Bearer {admin_token}"}


@pytest.fixture
def manager_headers(manager_token):
    return {"Authorization": f"Bearer {manager_token}"}


@pytest.fixture
def emp1_headers(emp1_token):
    return {"Authorization": f"Bearer {emp1_token}"}


@pytest.fixture
def emp2_headers(emp2_token):
    return {"Authorization": f"Bearer {emp2_token}"}


@pytest.fixture
def emp3_headers(emp3_token):
    return {"Authorization": f"Bearer {emp3_token}"}