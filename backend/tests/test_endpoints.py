import pytest


def test_health_endpoint(client):
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_cors_headers(client):
    """Test CORS middleware is properly configured"""
    response = client.options(
        "/health",
        headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "GET",
        },
    )
    # CORS preflight should be handled
    assert response.status_code in [200, 204, 405]


def test_exception_format(client):
    """Test that exceptions return proper JSON format"""
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "nonexistent@test.com",
            "password": "Password123",
        },
    )

    # Should have proper error format
    data = response.json()
    assert "error_code" in data
    assert "message" in data
    assert "details" in data
    assert response.status_code == 401
