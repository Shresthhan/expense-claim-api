def test_admin_can_delete_user(client, admin_headers):
    register_response = client.post(
        "/auth/register",
        json={
            "email": "delete_me@test.com",
            "password": "DeleteMe@123",
        },
    )
    assert register_response.status_code in (200, 201)

    created_user = register_response.json()
    user_id = created_user["id"]

    delete_response = client.delete(f"/users/{user_id}", headers=admin_headers)

    assert delete_response.status_code in (200, 204)


def test_employee_cannot_delete_user(client, emp1_headers):
    register_response = client.post(
        "/auth/register",
        json={
            "email": "cant_delete@test.com",
            "password": "DeleteMe@123",
        },
    )
    assert register_response.status_code in (200, 201)

    created_user = register_response.json()
    user_id = created_user["id"]

    delete_response = client.delete(f"/users/{user_id}", headers=emp1_headers)

    assert delete_response.status_code == 403