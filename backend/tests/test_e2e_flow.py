from datetime import date
from decimal import Decimal

from app.models.customer import Customer

NAME = "FlowCo"
EMAIL = "flow@flowco.com"
PASSWORD = "Passw0rd!"


def test_validation_error_shape(client):
    resp = client.post("/api/v1/auth/register", json={"email": "not-an-email"})
    assert resp.status_code == 422
    body = resp.json()
    assert body.get("error_code") == "VALIDATION_ERROR"
    assert body.get("message")
    assert isinstance(body.get("details"), list)


def test_full_product_flow(client, db_session):
    # 1. Register a brand-new company + admin.
    register = client.post(
        "/api/v1/auth/register",
        json={
            "sector": "telecom",
            "company_name": NAME,
            "subscription_tier": "pilot",
            "full_name": "Flow User",
            "email": EMAIL,
            "password": PASSWORD,
        },
    )
    assert register.status_code == 200
    token = register.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. /auth/me resolves the company.
    me = client.get("/api/v1/auth/me", headers=headers)
    assert me.status_code == 200
    me_body = me.json()
    assert me_body["company_name"] == NAME
    assert me_body["sector"] == "telecom"

    # 3. Dashboard stays consistent with an (empty) company.
    dash = client.get("/api/v1/dashboard/summary", headers=headers)
    assert dash.status_code == 200
    metrics = {m["id"]: m for m in dash.json()["overviewMetrics"]}
    assert metrics["conversations"]["value"] == 0

    # 4. Bootstrapping a customer for the new company.
    customer = Customer(
        company_id=me_body["company_id"],
        name="Flow Customer",
        phone="0790000001",
        current_plan="20GB Mobile Data",
        usage_percentage=Decimal("92.00"),
        contract_end_date=date(2026, 12, 31),
        segment="Heavy User",
        service_type="mobile_data",
    )
    db_session.add(customer)
    db_session.commit()
    customer_id = customer.id

    customers = client.get("/api/v1/customers", headers=headers)
    assert customers.status_code == 200
    assert len(customers.json()) == 1

    # 5. Chat uses the agent (rule-based fallback without GROQ_API_KEY).
    chat = client.post(
        "/api/v1/chat",
        json={"customer_id": customer_id, "message": "I need more data"},
        headers=headers,
    )
    assert chat.status_code == 200
    assert chat.json()["response"]

    # 6. The conversation created by the chat shows up in the inbox.
    conversations = client.get("/api/v1/conversations", headers=headers)
    assert conversations.status_code == 200
    assert len(conversations.json()) >= 1
    detail = client.get(
        f"/api/v1/conversations/{conversations.json()[0]['id']}", headers=headers
    )
    assert detail.status_code == 200
    assert detail.json()["customer"]["name"] == "Flow Customer"

    # 7. The dashboard now reflects the new conversation.
    dash_after = client.get("/api/v1/dashboard/summary", headers=headers)
    metrics_after = {m["id"]: m for m in dash_after.json()["overviewMetrics"]}
    assert metrics_after["conversations"]["value"] == 1

    # 8. Profile is editable.
    patched = client.patch(
        "/api/v1/auth/me",
        json={"full_name": "Renamed Admin", "sector": "banking"},
        headers=headers,
    )
    assert patched.status_code == 200
    assert patched.json()["full_name"] == "Renamed Admin"
    assert patched.json()["sector"] == "banking"