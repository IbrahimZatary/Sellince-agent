from datetime import date
from decimal import Decimal

from app.core.security import create_access_token
from app.models.company import Company
from app.models.conversation import Conversation
from app.models.customer import Customer
from app.models.message import Message
from app.models.offer import Offer
from app.models.user import User


def _seed_company(db_session, name="ConvCo", email="conv@convco.com"):
    company = Company(name=name, sector="telecom", subscription_tier="standard")
    db_session.add(company)
    db_session.flush()
    user = User(
        company_id=company.id,
        full_name="Conv User",
        email=email,
        password_hash="not-used-in-test",
        role="admin",
    )
    db_session.add(user)
    db_session.flush()
    return company, user


def _seed_conversation(db_session, company, name="Dana", plan="20GB Mobile Data"):
    customer = Customer(
        company_id=company.id,
        name=name,
        phone="0790000001",
        current_plan=plan,
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
            Message(conversation_id=conversation.id, sender="customer", text="I need more data"),
            Message(conversation_id=conversation.id, sender="agent", text="How about the 50GB plan?"),
        ]
    )
    offer = Offer(
        customer_id=customer.id,
        conversation_id=conversation.id,
        company_id=company.id,
        product_name="50GB Mobile 5G",
        price=Decimal("25.00"),
        status="sent",
    )
    db_session.add(offer)
    db_session.commit()
    return customer.id


def test_list_conversations_requires_auth(client, db_session):
    resp = client.get("/api/v1/conversations")
    assert resp.status_code == 401


def test_list_and_detail(client, db_session):
    company, user = _seed_company(db_session)
    _seed_conversation(db_session, company)
    token = create_access_token({"sub": str(user.id)})
    headers = {"Authorization": f"Bearer {token}"}

    resp = client.get("/api/v1/conversations", headers=headers)
    assert resp.status_code == 200
    items = resp.json()
    assert len(items) == 1

    item = items[0]
    assert item["status"] == "open"
    assert item["message_count"] == 2
    assert item["customer"]["name"] == "Dana"
    assert item["last_message"]["text"] == "How about the 50GB plan?"
    assert item["offer"]["product_name"] == "50GB Mobile 5G"

    detail_resp = client.get(f"/api/v1/conversations/{item['id']}", headers=headers)
    assert detail_resp.status_code == 200
    detail = detail_resp.json()
    assert len(detail["messages"]) == 2
    assert detail["messages"][0]["sender"] == "customer"
    assert detail["offer"]["price"] == "25.00"


def test_detail_unknown_conversation(client, db_session):
    company, user = _seed_company(db_session)
    _seed_conversation(db_session, company)
    token = create_access_token({"sub": str(user.id)})
    headers = {"Authorization": f"Bearer {token}"}

    resp = client.get("/api/v1/conversations/99999", headers=headers)
    assert resp.status_code == 404
    assert resp.json().get("error_code") == "CONVERSATION_NOT_FOUND"


def test_detail_cross_tenant_conversation(client, db_session):
    company, user = _seed_company(db_session)
    other_company, _ = _seed_company(
        db_session, name="OtherCo", email="other@otherco.com"
    )
    _seed_conversation(db_session, other_company, name="Zaid")
    token = create_access_token({"sub": str(user.id)})
    headers = {"Authorization": f"Bearer {token}"}

    other_conv = (
        db_session.query(Conversation)
        .filter(Conversation.company_id == other_company.id)
        .first()
    )
    resp = client.get(f"/api/v1/conversations/{other_conv.id}", headers=headers)
    assert resp.status_code == 404
    assert resp.json().get("error_code") == "CONVERSATION_NOT_FOUND"