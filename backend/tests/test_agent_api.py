from datetime import date
from decimal import Decimal

from app.models.company import Company
from app.models.customer import Customer


def test_chat_no_auth_required(client, db_session):
    """Chat works without auth: customer_id in body -> AI reply."""
    company = Company(name="TestCo", sector="telecom", subscription_tier="standard")
    db_session.add(company)
    db_session.flush()

    customer = Customer(
        company_id=company.id,
        name="Test Customer",
        phone="0790000001",
        current_plan="5GB Data Plan",
        usage_percentage=Decimal("95.00"),
        contract_end_date=date(2026, 12, 31),
        segment="Heavy User",
    )
    db_session.add(customer)
    db_session.flush()
    db_session.commit()

    response = client.post(
        "/api/v1/chat",
        json={"customer_id": customer.id, "message": "I need more data"}
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
    response = client.post(
        "/api/v1/chat", json={"customer_id": 99999, "message": "hello"}
    )

    assert response.status_code == 404
    assert response.json().get("error_code") == "CUSTOMER_NOT_FOUND"


def test_chat_cross_tenant_allowed(client, db_session):
    """Any customer_id works (no tenant isolation for embeddable widget)."""
    # Create two companies with customers
    company1 = Company(name="Company1", sector="telecom", subscription_tier="standard")
    company2 = Company(name="Company2", sector="telecom", subscription_tier="pilot")
    db_session.add_all([company1, company2])
    db_session.flush()

    customer1 = Customer(
        company_id=company1.id,
        name="Customer1",
        phone="0790000001",
        current_plan="5GB Data Plan",
        usage_percentage=Decimal("95.00"),
        contract_end_date=date(2026, 12, 31),
        segment="Heavy User",
    )
    customer2 = Customer(
        company_id=company2.id,
        name="Customer2",
        phone="0790000002",
        current_plan="5GB Data Plan",
        usage_percentage=Decimal("50.00"),
        contract_end_date=date(2026, 12, 31),
        segment="Average User",
    )
    db_session.add_all([customer1, customer2])
    db_session.commit()

    # Customer from company2 can be accessed (no tenant fence)
    response = client.post(
        "/api/v1/chat",
        json={"customer_id": customer2.id, "message": "hello"}
    )
    assert response.status_code == 200


def test_chat_missing_fields(client, db_session):
    """Request validation still applies."""
    resp = client.post("/api/v1/chat", json={"customer_id": 1})
    assert resp.status_code == 422

    resp = client.post("/api/v1/chat", json={"message": "hello"})
    assert resp.status_code == 422


def test_chat_invalid_types(client, db_session):
    """Invalid field types are rejected with 422."""
    payload = {"customer_id": "not_an_int", "message": "hello"}
    resp = client.post("/api/v1/chat", json=payload)
    assert resp.status_code == 422