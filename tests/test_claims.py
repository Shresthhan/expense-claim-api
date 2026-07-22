"""Tests for claim endpoints."""
def test_employee_cannot_view_another_employee_claim(client, emp1_headers, emp2_headers):
    claims_response = client.get("/claims", headers=emp2_headers)
    assert claims_response.status_code == 200

    emp2_claims = claims_response.json()
    assert len(emp2_claims) > 0

    emp2_claim_id = emp2_claims[0]["id"]

    response = client.get(f"/claims/{emp2_claim_id}", headers=emp1_headers)

    assert response.status_code == 403


def test_manager_can_view_direct_report_claim(client, manager_headers, emp1_headers):
    claims_response = client.get("/claims", headers=emp1_headers)
    assert claims_response.status_code == 200

    emp1_claims = claims_response.json()
    assert len(emp1_claims) > 0

    emp1_claim_id = emp1_claims[0]["id"]

    response = client.get(f"/claims/{emp1_claim_id}", headers=manager_headers)

    assert response.status_code == 200
    assert response.json()["id"] == emp1_claim_id


def test_manager_cannot_view_unrelated_employee_claim(client, manager_headers, emp3_headers):
    claims_response = client.get("/claims", headers=emp3_headers)
    assert claims_response.status_code == 200

    emp3_claims = claims_response.json()
    assert len(emp3_claims) > 0

    emp3_claim_id = emp3_claims[0]["id"]

    response = client.get(f"/claims/{emp3_claim_id}", headers=manager_headers)

    assert response.status_code == 403