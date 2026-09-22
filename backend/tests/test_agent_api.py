from datetime import date
from decimal import Decimal

from app.models.company import Company
from app.models.customer import Customer
from app.models.attribution import Attribution


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


def test_chat_returns_purchase_action_for_checkout_flow(client, db_session):
    """When the customer is ready to pay, the chatbot returns a purchase action with a checkout URL."""
    company = Company(name="FlowCo", sector="telecom", subscription_tier="standard")
    db_session.add(company)
    db_session.flush()

    customer = Customer(
        company_id=company.id,
        name="Paying Customer",
        phone="0790000009",
        current_plan="20GB Mobile Data",
        usage_percentage=Decimal("92.00"),
        contract_end_date=date(2026, 12, 31),
        segment="Heavy User",
        service_type="mobile_data",
    )
    db_session.add(customer)
    db_session.flush()
    db_session.commit()

    response = client.post(
        "/api/v1/chat",
        json={"customer_id": customer.id, "message": "I want to pay now"},
    )

    assert response.status_code == 200
    data = response.json()
    action = data["action"]
    assert isinstance(action, dict)
    assert action["type"] == "purchase"
    assert action["label"] == "Continue to Purchase"
    assert "/checkout?" in action["url"]
    assert f"customer_id={customer.id}" in action["url"]
    assert "conversation_id=" in action["url"]
    assert "product_id=" in action["url"]
    assert "attribution_id=" in action["url"]

    pending = db_session.query(Attribution).one()
    assert pending.status == "pending"

    completed = client.post(
        "/api/v1/attributions/checkout/complete",
        json={
            "customer_id": customer.id,
            "conversation_id": int(action["url"].split("conversation_id=")[1].split("&")[0]),
            "product_id": action["url"].split("product_id=")[1].split("&")[0],
        },
    )
    assert completed.status_code == 200
    assert completed.json()["status"] == "completed"
    db_session.refresh(customer)
    assert customer.current_plan == pending.product_name
    assert customer.usage_percentage == Decimal("0.00")
    assert customer.contract_end_date == date(2026, 12, 31)


def test_accepted_offer_returns_purchase_action(client, db_session):
    company = Company(name="AcceptedCo", sector="telecom", subscription_tier="standard")
    db_session.add(company)
    db_session.flush()

    customer = Customer(
        company_id=company.id,
        name="Accepted Customer",
        phone="0790000011",
        current_plan="20GB Mobile Data",
        usage_percentage=Decimal("92.00"),
        contract_end_date=date(2026, 12, 31),
        segment="Heavy User",
        service_type="mobile_data",
    )
    db_session.add(customer)
    db_session.commit()

    response = client.post(
        "/api/v1/chat",
        json={"customer_id": customer.id, "message": "okay i want"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["conversation_stage"] == "CLOSE_DEAL"
    assert data["action"]["type"] == "purchase"
    assert data["action"]["label"] == "Continue to Purchase"
    assert "product_id=" in data["action"]["url"]
    assert "/mock/product" not in data["response"]