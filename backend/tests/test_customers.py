from datetime import date
from decimal import Decimal

from app.core.security import create_access_token
from app.models.company import Company
from app.models.customer import Customer
from app.models.user import User


def _seed(db_session):
    company = Company(name="CustCo", sector="telecom", subscription_tier="standard")
    db_session.add(company)
    db_session.flush()
    user = User(
        company_id=company.id,
        full_name="Cust User",
        email="cust@custco.com",
        password_hash="not-used-in-test",
        role="admin",
    )
    db_session.add(user)
    db_session.flush()
    db_session.add_all(
        [
            Customer(
                company_id=company.id,
                name="Dana",
                phone="0790000001",
                current_plan="20GB Mobile Data",
                usage_percentage=Decimal("90.00"),
                contract_end_date=date(2027, 1, 1),
                segment="Heavy User",
            ),
            Customer(
                company_id=company.id,
                name="Zaid",
                phone="0790000002",
                current_plan="Fiber 100 Mbps",
                usage_percentage=Decimal("40.00"),
                contract_end_date=date(2026, 12, 1),
                segment="Average User",
            ),
        ]
    )
    db_session.commit()
    token = create_access_token({"sub": str(user.id)})
    return {"Authorization": f"Bearer {token}"}


def test_customers_requires_auth(client, db_session):
    resp = client.get("/api/v1/customers")
    assert resp.status_code == 401


def test_customers_list_and_tenant_scope(client, db_session):
    headers = _seed(db_session)
    resp = client.get("/api/v1/customers", headers=headers)
    assert resp.status_code == 200
    customers = resp.json()
    assert len(customers) == 2
    assert customers[0]["name"] == "Dana"
    assert customers[1]["current_plan"] == "Fiber 100 Mbps"
    fields = {"id", "name", "phone", "current_plan", "service_type", "segment"}
    assert set(customers[0]) == fields

    other_company = Company(name="OtherCo", sector="telecom", subscription_tier="pilot")
    db_session.add(other_company)
    db_session.flush()
    db_session.add(
        Customer(
            company_id=other_company.id,
            name="Hiding",
            phone="0790000099",
            current_plan="5G Data",
            usage_percentage=Decimal("10.00"),
            contract_end_date=None,
        )
    )
    db_session.commit()

    resp_again = client.get("/api/v1/customers", headers=headers)
    assert len(resp_again.json()) == 2