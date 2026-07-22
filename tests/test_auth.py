"""Tests for auth endpoints."""
def test_login_returns_access_token(client):
    response = client.post(
        "/auth/login",
        json={
            "email": "emp1@test.com",
            "password": "Emp@123",
        },
    )

    assert response.status_code == 200

    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_missing_token_returns_401(client):
    response = client.get("/me")

    assert response.status_code == 401


def test_invalid_token_returns_401(client):
    response = client.get(
        "/me",
        headers={"Authorization": "Bearer invalid-token"},
    )

    assert response.status_code == 401