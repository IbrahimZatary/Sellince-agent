from unittest.mock import MagicMock
import pytest
from graph import compiled_graph


def create_mock_db(customer=None):
    """Helper to mock SQLAlchemy Session query chain."""
    mock_db = MagicMock()
    mock_db.query.return_value.filter.return_value.first.return_value = customer
    return mock_db


# ---------------------------------------------------------------------
# Scenario 1: High-Usage Customer Triggering an Upsell Flow
# ---------------------------------------------------------------------
def test_graph_e2e_high_usage_upsell():
    """Customer with >90% usage asking about internet speed receives an offer."""
    mock_customer = MagicMock()
    mock_customer.id = 1
    mock_customer.name = "Sara"
    mock_customer.current_plan = "5GB Data Plan"
    mock_customer.usage_percentage = 95.0
    mock_customer.segment = "retail"

    mock_db = create_mock_db(customer=mock_customer)

    initial_state = {
        "customer_id": 1,
        "message": "My connection is very slow, did my data run out?",
        "_db": mock_db,
    }

    # Execute full LangGraph pipeline
    final_state = compiled_graph.invoke(initial_state)

    # 1. State integrity checks
    assert "customer_data" in final_state
    assert final_state["customer_data"]["name"] == "Sara"

    # 2. Recommendation verification
    assert final_state.get("recommendation") is not None
    assert "primary" in final_state["recommendation"]
    assert isinstance(final_state["recommendation"]["primary"], dict)

    # 3. Response verification
    assert "response" in final_state
    assert isinstance(final_state["response"], str)
    assert len(final_state["response"]) > 0

    # 4. Action verification
    assert final_state.get("action") in ["offer", "recommend"]


# ---------------------------------------------------------------------
# Scenario 2: Normal Usage / Standard Inquiry
# ---------------------------------------------------------------------
def test_graph_e2e_normal_usage_inquiry():
    """Customer with low usage asking a general question."""
    mock_customer = MagicMock()
    mock_customer.id = 2
    mock_customer.name = "Ahmad"
    mock_customer.current_plan = "50GB Ultra Plan"
    mock_customer.usage_percentage = 20.0
    mock_customer.segment = "retail"

    mock_db = create_mock_db(customer=mock_customer)

    initial_state = {
        "customer_id": 2,
        "message": "How do I check my bill due date?",
        "_db": mock_db,
    }

    final_state = compiled_graph.invoke(initial_state)

    assert final_state.get("customer_data") is not None
    assert final_state["customer_data"]["name"] == "Ahmad"
    assert "response" in final_state
    assert len(final_state["response"]) > 0


# ---------------------------------------------------------------------
# Scenario 3: Non-Existent Customer Edge Case
# ---------------------------------------------------------------------
def test_graph_e2e_customer_not_found():
    """Invalid customer ID gracefully routes to abort/fallback."""
    mock_db = create_mock_db(customer=None)

    initial_state = {
        "customer_id": 99999,
        "message": "Hello",
        "_db": mock_db,
    }

    final_state = compiled_graph.invoke(initial_state)

    # Customer data should remain None
    assert final_state.get("customer_data") is None
    # Graph should output a fallback message or set an abort action
    assert "response" in final_state or final_state.get("action") == "abort"    