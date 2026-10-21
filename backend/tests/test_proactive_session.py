
from unittest.mock import patch

from app.models.company import Company
from app.models.customer import Customer
from app.models.message import Message
from app.models.offer import Offer

from unittest.mock import patch

from app.models.company import Company
from app.models.customer import Customer
from app.models.conversation import Conversation
from app.models.message import Message
from app.models.offer import Offer


def test_returning_customer_does_not_repeat_offer(client, db_session):
    company = Company(
        name="Returning Test Co",
        sector="telecom",
        subscription_tier="standard",
    )
    db_session.add(company)
    db_session.flush()

    customer = Customer(
        company_id=company.id,
        name="Returning Customer",
        phone="0799999922",
        service_type="mobile_data",
        current_plan="20GB Mobile Data",
        usage_percentage=95,
        segment="Heavy User",
    )
    db_session.add(customer)
    db_session.flush()

    conversation = Conversation(
        customer_id=customer.id,
        company_id=company.id,
        status="open",
    )
    db_session.add(conversation)
    db_session.commit()

    with (
        patch(
            "app.api.agent_session.has_existing_checkpoint",
            return_value=True,
        ),
        patch(
            "app.api.agent_session.run_proactive_session",
        ) as mock_run,
    ):
        response = client.post(
            "/api/v1/agent/start-session",
            json={"customer_id": customer.id},
        )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "existing"
    assert data["conversation_id"] == conversation.id
    assert data["response"] is None
    assert data["offer"] is None

    mock_run.assert_not_called()

    assert db_session.query(Message).count() == 0
    assert db_session.query(Offer).count() == 0


def test_first_time_customer_proactive_session(client, db_session):
    company = Company(
        name="Proactive Test Co",
        sector="telecom",
        subscription_tier="standard",
    )
    db_session.add(company)
    db_session.flush()

    customer = Customer(
        company_id=company.id,
        name="Proactive Customer",
        phone="0799999911",
        service_type="mobile_data",
        current_plan="20GB Mobile Data",
        usage_percentage=95,
        segment="Heavy User",
    )
    db_session.add(customer)
    db_session.commit()

    mock_result = {
        "response": "You're using 95% of your data. Would you like to upgrade?",
        "active_offer": {
            "product_id": 1,
            "product_name": "50GB Mobile 5G",
            "price": 25,
        },
    }

    with (
        patch(
            "app.api.agent_session.has_existing_checkpoint",
            return_value=False,
        ),
        patch(
            "app.api.agent_session.run_proactive_session",
            return_value=mock_result,
        ),
    ):
        response = client.post(
            "/api/v1/agent/start-session",
            json={"customer_id": customer.id},
        )

    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "started"
    assert data["offer"]["product_name"] == "50GB Mobile 5G"

    messages = db_session.query(Message).all()
    offers = db_session.query(Offer).all()

    assert len(messages) == 1
    assert messages[0].sender == "agent"
    assert messages[0].text == mock_result["response"]

    assert len(offers) == 1
    assert offers[0].customer_id == customer.id
    assert offers[0].product_name == "50GB Mobile 5G"

def test_start_session_customer_not_found(client):
    response = client.post(
        "/api/v1/agent/start-session",
        json={"customer_id": 99999},
    )

    assert response.status_code == 404
    assert response.json()["error_code"] == "CUSTOMER_NOT_FOUND"


def test_start_session_missing_customer_id(client):
    response = client.post(
        "/api/v1/agent/start-session",
        json={},
    )

    assert response.status_code == 422
