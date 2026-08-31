import pytest


def test_register_success(client):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "sector": "telecom",
            "password": "SecurePass123!",
            "company_name": "TeleCorp",
            "full_name": "John Doe",
            "email": "john@telecorp.com",
            "subscription_tier": "standard",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_register_duplicate_email(client):
    # Register first user
    client.post(
        "/api/v1/auth/register",
        json={
            "sector": "telecom",
            "password": "Pass123456!",
            "company_name": "Corp1",
            "full_name": "User1",
            "email": "same@email.com",
            "subscription_tier": "standard",
        },
    )

    # Try to register same email
    response = client.post(
        "/api/v1/auth/register",
        json={
            "sector": "banking",
            "password": "Pass123456!",
            "company_name": "Corp2",
            "full_name": "User2",
            "email": "same@email.com",
            "subscription_tier": "enterprise",
        },
    )
    assert response.status_code == 409
    assert response.json()["error_code"] == "EMAIL_EXISTS"


def test_register_weak_password(client):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "sector": "telecom",
            "password": "weak",  # < 8 chars
            "company_name": "Corp",
            "full_name": "User",
            "email": "user@corp.com",
            "subscription_tier": "standard",
        },
    )
    assert response.status_code == 422  # Validation error


def test_register_invalid_sector(client):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "sector": "invalid_sector",
            "password": "SecurePass123!",
            "company_name": "Corp",
            "full_name": "User",
            "email": "user@corp.com",
            "subscription_tier": "standard",
        },
    )
    assert response.status_code == 422  # Validation error


def test_register_invalid_email(client):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "sector": "telecom",
            "password": "SecurePass123!",
            "company_name": "Corp",
            "full_name": "User",
            "email": "not_an_email",
            "subscription_tier": "standard",
        },
    )
    assert response.status_code == 422  # Validation error


def test_login_success(client):
    # Register
    client.post(
        "/api/v1/auth/register",
        json={
            "sector": "telecom",
            "password": "SecurePass123!",
            "company_name": "TeleCorp",
            "full_name": "John Doe",
            "email": "john@telecorp.com",
            "subscription_tier": "standard",
        },
    )

    # Login
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "john@telecorp.com",
            "password": "SecurePass123!",
        },
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_wrong_password(client):
    # Register
    client.post(
        "/api/v1/auth/register",
        json={
            "sector": "telecom",
            "password": "SecurePass123!",
            "company_name": "TeleCorp",
            "full_name": "John Doe",
            "email": "john@telecorp.com",
            "subscription_tier": "standard",
        },
    )

    # Try wrong password
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "john@telecorp.com",
            "password": "WrongPassword",
        },
    )
    assert response.status_code == 401
    assert response.json()["error_code"] == "INVALID_CREDENTIALS"


def test_login_nonexistent_user(client):
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "nobody@nowhere.com",
            "password": "SomePass123",
        },
    )
    assert response.status_code == 401
    assert response.json()["error_code"] == "INVALID_CREDENTIALS"


def test_login_banking_sector(client):
    # Register with banking sector
    client.post(
        "/api/v1/auth/register",
        json={
            "sector": "banking",
            "password": "BankPass123!",
            "company_name": "FirstBank",
            "full_name": "Jane Smith",
            "email": "jane@bank.com",
            "subscription_tier": "enterprise",
        },
    )

    # Login should work
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "jane@bank.com",
            "password": "BankPass123!",
        },
    )
    assert response.status_code == 200


def test_auth_me_missing_token_uses_error_contract(client):
    response = client.get("/api/v1/auth/me")

    assert response.status_code == 401
    assert response.json() == {
        "error_code": "MISSING_TOKEN",
        "message": "Authentication token is required",
        "details": None,
    }
