from datetime import date
from decimal import Decimal

from app.core.security import create_access_token
from app.models.company import Company
from app.models.conversation import Conversation
from app.models.customer import Customer
from app.models.message import Message
from app.models.offer import Offer
from app.models.user import User


def _seed_dashboard(db_session):
    company = Company(name="DashCo", sector="telecom", subscription_tier="standard")
    db_session.add(company)
    db_session.flush()
    user = User(
        company_id=company.id,
        full_name="Dash User",
        email="dash@dashco.com",
        password_hash="not-used-in-test",
        role="admin",
    )
    db_session.add(user)
    db_session.flush()
    customer = Customer(
        company_id=company.id,
        name="Dana",
        phone="0790000001",
        current_plan="20GB Mobile Data",
        usage_percentage=Decimal("90.00"),
        contract_end_date=date(2027, 1, 1),
        segment="Heavy User",
        service_type="mobile_data",
    )
    db_session.add(customer)
    db_session.flush()
    conversation = Conversation(
        customer_id=customer.id, company_id=company.id, status="open"
    )
    db_session.add(conversation)
    db_session.flush()
    db_session.add_all(
        [
            Offer(
                customer_id=customer.id,
                conversation_id=conversation.id,
                company_id=company.id,
                product_name="50GB Mobile 5G",
                price=Decimal("25.00"),
                status="accepted",
            ),
            Offer(
                customer_id=customer.id,
                conversation_id=conversation.id,
                company_id=company.id,
                product_name="5G Add-on",
                price=Decimal("5.00"),
                status="sent",
            ),
        ]
    )
    db_session.add_all(
        [
            Message(conversation_id=conversation.id, sender="agent", text="Hello Dana"),
            Message(conversation_id=conversation.id, sender="customer", text="Hi"),
        ]
    )
    db_session.commit()
    token = create_access_token({"sub": str(user.id)})
    return {"Authorization": f"Bearer {token}"}


def test_dashboard_requires_auth(client, db_session):
    resp = client.get("/api/v1/dashboard/summary")
    assert resp.status_code == 401


def test_dashboard_summary_shape_and_counts(client, db_session):
    headers = _seed_dashboard(db_session)

    resp = client.get("/api/v1/dashboard/summary", headers=headers)
    assert resp.status_code == 200

    body = resp.json()
    assert set(
        [
            "overviewMetrics",
            "revenueTrend",
            "conversionFunnel",
            "revenueByOffer",
            "agentAutonomy",
            "recentActivity",
        ]
    ) <= set(body)

    metrics = {m["id"]: m for m in body["overviewMetrics"]}
    assert metrics["conversations"]["value"] == 1
    assert metrics["offers"]["value"] == 2
    assert metrics["conversion"]["value"] == "50%"
    assert metrics["customers"]["value"] == 1

    assert len(body["revenueTrend"]) == 7
    assert body["conversionFunnel"][0]["stage"] == "Engaged"
    assert body["conversionFunnel"][1]["percentage"] == 100  # replied (2 msgs)

    shares = {s["category"]: s["value"] for s in body["revenueByOffer"]}
    assert shares["Data Upgrades"] == 50
    assert shares["Add-ons"] == 50

    assert body["recentActivity"][0]["customer"] == "Dana"
    assert body["recentActivity"][0]["status"] == "open"