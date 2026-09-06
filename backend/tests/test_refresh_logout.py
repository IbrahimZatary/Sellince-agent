from datetime import timedelta

from app.api.auth import utc_now
from app.core.security import generate_opaque_token, hash_opaque_token
from app.models.refresh_token import RefreshToken

REGISTER_BODY = {
    "sector": "telecom",
    "password": "SecurePass123!",
    "company_name": "RefreshCorp",
    "full_name": "Refresh User",
    "email": "refresh@corp.com",
    "subscription_tier": "standard",
}


def _register(client):
    return client.post("/api/v1/auth/register", json=REGISTER_BODY)


def test_auth_me_with_valid_token(client):
    register_resp = _register(client)
    token = register_resp.json()["access_token"]

    response = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == REGISTER_BODY["email"]
    assert data["full_name"] == REGISTER_BODY["full_name"]
    assert data["role"] == "admin"
    assert data["company_name"] == REGISTER_BODY["company_name"]


def test_refresh_rotates_and_sets_new_cookie(client):
    register_resp = _register(client)
    assert register_resp.status_code == 200
    old_cookie = register_resp.cookies.get("refresh_token")
    assert old_cookie

    client.cookies.set("refresh_token", old_cookie)
    response = client.post("/api/v1/auth/refresh")
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"
    new_cookie = response.cookies.get("refresh_token")
    assert new_cookie
    assert new_cookie != old_cookie


def test_refresh_rejects_reused_token(client):
    register_resp = _register(client)
    old_cookie = register_resp.cookies.get("refresh_token")

    client.cookies.set("refresh_token", old_cookie)
    first = client.post("/api/v1/auth/refresh")
    assert first.status_code == 200

    client.cookies.set("refresh_token", old_cookie)
    second = client.post("/api/v1/auth/refresh")
    assert second.status_code == 401
    assert second.json()["error_code"] == "REFRESH_TOKEN_REVOKED"


def test_refresh_missing_cookie(client):
    client.cookies.clear()
    response = client.post("/api/v1/auth/refresh")
    assert response.status_code == 401
    assert response.json()["error_code"] == "MISSING_REFRESH_TOKEN"


def test_refresh_invalid_cookie(client):
    client.cookies.set("refresh_token", "not-a-real-token")
    response = client.post("/api/v1/auth/refresh")
    assert response.status_code == 401
    assert response.json()["error_code"] == "INVALID_REFRESH_TOKEN"


def test_refresh_expired_token(client, db_session):
    register_resp = _register(client)
    token = register_resp.json()["access_token"]
    user_id = client.get(
        "/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"}
    ).json()["id"]

    raw_token = generate_opaque_token()
    expired_record = RefreshToken(
        user_id=user_id,
        token_hash=hash_opaque_token(raw_token),
        expires_at=utc_now() - timedelta(days=1),
    )
    db_session.add(expired_record)
    db_session.commit()

    client.cookies.set("refresh_token", raw_token)
    response = client.post("/api/v1/auth/refresh")
    assert response.status_code == 401
    assert response.json()["error_code"] == "REFRESH_TOKEN_EXPIRED"


def test_logout_revokes_token_and_clears_cookie(client):
    register_resp = _register(client)
    old_cookie = register_resp.cookies.get("refresh_token")
    assert old_cookie

    client.cookies.set("refresh_token", old_cookie)
    response = client.post("/api/v1/auth/logout")
    assert response.status_code == 200
    assert response.json()["message"] == "Successfully logged out"

    client.cookies.set("refresh_token", old_cookie)
    refreshed = client.post("/api/v1/auth/refresh")
    assert refreshed.status_code == 401


def test_logout_without_cookie_is_success(client):
    client.cookies.clear()
    response = client.post("/api/v1/auth/logout")
    assert response.status_code == 200
    assert response.json()["message"] == "Successfully logged out"
