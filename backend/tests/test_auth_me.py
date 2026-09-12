from app.core.security import create_access_token
from app.models.company import Company
from app.models.user import User


def _seed(db_session):
    company = Company(name="MeCo", sector="telecom", subscription_tier="standard")
    db_session.add(company)
    db_session.flush()
    user = User(
        company_id=company.id,
        full_name="Me User",
        email="me@meco.com",
        password_hash="not-used-in-test",
        role="admin",
    )
    db_session.add(user)
    db_session.commit()
    token = create_access_token({"sub": str(user.id)})
    return {"Authorization": f"Bearer {token}"}


def test_me_requires_auth(client, db_session):
    resp = client.patch("/api/v1/auth/me", json={"full_name": "X"})
    assert resp.status_code == 401


def test_me_returns_company_fields(client, db_session):
    headers = _seed(db_session)
    resp = client.get("/api/v1/auth/me", headers=headers)
    assert resp.status_code == 200
    body = resp.json()
    assert body["company_name"] == "MeCo"
    assert body["sector"] == "telecom"
    assert body["subscription_tier"] == "standard"


def test_me_update_profile(client, db_session):
    headers = _seed(db_session)
    resp = client.patch(
        "/api/v1/auth/me",
        json={
            "full_name": "New Name",
            "company_name": "RenamedCo",
            "sector": "banking",
            "subscription_tier": "enterprise",
        },
        headers=headers,
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["full_name"] == "New Name"
    assert body["company_name"] == "RenamedCo"
    assert body["sector"] == "banking"
    assert body["subscription_tier"] == "enterprise"
    assert body["email"] == "me@meco.com"


def test_me_partial_update(client, db_session):
    headers = _seed(db_session)
    resp = client.patch("/api/v1/auth/me", json={"full_name": "Just My Name"}, headers=headers)
    assert resp.status_code == 200
    body = resp.json()
    assert body["full_name"] == "Just My Name"
    assert body["sector"] == "telecom"
    assert body["subscription_tier"] == "standard"


def test_me_rejects_invalid_sector(client, db_session):
    headers = _seed(db_session)
    resp = client.patch("/api/v1/auth/me", json={"sector": "insurance"}, headers=headers)
    assert resp.status_code == 422