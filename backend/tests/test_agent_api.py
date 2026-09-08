from datetime import date
from decimal import Decimal

from app.core.security import create_access_token
from app.models.company import Company
from app.models.customer import Customer
from app.models.user import User

client_seed = {}


def _auth_headers(db_session):
    company = Company(name="TestCo", sector="telecom", subscription_tier="standard")
    db_session.add(company)
    db_session.flush()
    user = User(
        company_id=company.id,
        full_name="Test Agent",
        email="agent@testco.com",
        password_hash="not-used-in-test",
        role="admin",
    )
    db_session.add(user)
    db_session.flush()
    customer = Customer(
        company_id=company.id,
        name="Sara",
        phone="0790000001",
        current_plan="5GB Data Plan",
        usage_percentage=Decimal("95.00"),
        contract_end_date=date(2026, 12, 31),
        segment="Heavy User",
    )
    db_session.add(customer)
    db_session.flush()
    token = create_access_token({"sub": str(user.id)})
    return {"Authorization": f"Bearer {token}"}, customer.id


def test_chat_requires_auth(client, db_session):
    """Chat is protected: no token -> 401."""
    resp = client.post(
        "/api/v1/chat", json={"customer_id": 1, "message": "I need more data"}
    )
    assert resp.status_code == 401


def test_chat_valid_customer(client, db_session):
    """Valid, authenticated request for an existing customer returns a reply."""
    headers, customer_id = _auth_headers(db_session)
    response = client.post(
        "/api/v1/chat",
        json={"customer_id": customer_id, "message": "I need more data"},
        headers=headers,
    )

    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert "offer" in data
    assert "action" in data
    assert isinstance(data["response"], str)
    assert len(data["response"]) > 0


def test_chat_nonexistent_customer(client, db_session):
    """Unknown customer id is fenced with 404 (not found)."""
    headers, _ = _auth_headers(db_session)

    response = client.post(
        "/api/v1/chat", json={"customer_id": 99999, "message": "hello"}, headers=headers
    )

    assert response.status_code == 404
    assert response.json().get("error_code") == "CUSTOMER_NOT_FOUND"


def test_chat_cross_tenant_customer(client, db_session):
    """A customer from another company is invisible to this user (tenant fence)."""
    headers, _ = _auth_headers(db_session)

    other_company = Company(name="OtherCo", sector="telecom", subscription_tier="pilot")
    db_session.add(other_company)
    db_session.flush()
    other_customer = Customer(
        company_id=other_company.id,
        name="Zaid",
        phone="0790000099",
        current_plan="20GB Mobile Data",
        usage_percentage=Decimal("50.00"),
        contract_end_date=date(2027, 1, 1),
        segment="Average User",
    )
    db_session.add(other_customer)
    db_session.flush()

    response = client.post(
        "/api/v1/chat",
        json={"customer_id": other_customer.id, "message": "hello"},
        headers=headers,
    )

    assert response.status_code == 404
    assert response.json().get("error_code") == "CUSTOMER_NOT_FOUND"


def test_chat_missing_fields(client, db_session):
    """Request validation still applies after auth succeeds."""
    headers, _ = _auth_headers(db_session)

    resp = client.post("/api/v1/chat", json={"customer_id": 1}, headers=headers)
    assert resp.status_code == 422

    resp = client.post("/api/v1/chat", json={"message": "hello"}, headers=headers)
    assert resp.status_code == 422


def test_chat_invalid_types(client, db_session):
    """Invalid field types are rejected with 422 after auth."""
    headers, _ = _auth_headers(db_session)

    payload = {"customer_id": "not_an_int", "message": "hello"}
    resp = client.post("/api/v1/chat", json=payload, headers=headers)
    assert resp.status_code == 422