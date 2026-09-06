from datetime import date
from unittest.mock import MagicMock
import pytest
from fastapi.testclient import TestClient

from app.core.database import get_db
from main import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def cleanup_overrides():
    """Ensure dependency overrides are always cleaned up after each test."""
    yield
    app.dependency_overrides.clear()


# ---------------------------------------------------------------------
# 1. Valid Customer Test
# ---------------------------------------------------------------------
def test_chat_valid_customer():
    """Test valid chat request for an existing customer."""
    mock_customer = MagicMock()
    mock_customer.id = 1
    mock_customer.name = "Sara"
    mock_customer.phone = "0790000001"
    mock_customer.current_plan = "5GB Data Plan"
    mock_customer.usage_percentage = 95.0
    mock_customer.contract_end_date = date(2026, 12, 31)
    mock_customer.segment = "retail"

    mock_db = MagicMock()
    mock_db.query.return_value.filter.return_value.first.return_value = mock_customer

    app.dependency_overrides[get_db] = lambda: mock_db

    payload = {"customer_id": 1, "message": "I need more data"}
    response = client.post("/api/chat", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert "offer" in data
    assert "action" in data
    assert isinstance(data["response"], str)
    assert len(data["response"]) > 0


# ---------------------------------------------------------------------
# 2. Non-Existent Customer Test
# ---------------------------------------------------------------------
def test_chat_nonexistent_customer():
    """Test fallback handling when customer ID is not found."""
    mock_db = MagicMock()
    mock_db.query.return_value.filter.return_value.first.return_value = None

    app.dependency_overrides[get_db] = lambda: mock_db

    payload = {"customer_id": 99999, "message": "hello"}
    response = client.post("/api/chat", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert "offer" in data
    assert "action" in data


# ---------------------------------------------------------------------
# 3. Missing Fields Validation Test
# ---------------------------------------------------------------------
def test_chat_missing_fields():
    """Test request validation when required payload fields are missing."""
    # Missing 'message'
    response = client.post("/api/chat", json={"customer_id": 1})
    assert response.status_code == 422

    # Missing 'customer_id'
    response = client.post("/api/chat", json={"message": "hello"})
    assert response.status_code == 422


# ---------------------------------------------------------------------
# 4. Invalid Types Validation Test
# ---------------------------------------------------------------------
def test_chat_invalid_types():
    """Test request validation when fields have incorrect data types."""
    # String customer_id instead of int
    payload = {"customer_id": "not_an_int", "message": "hello"}
    response = client.post("/api/chat", json=payload)
    assert response.status_code == 422
