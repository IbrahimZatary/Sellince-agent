from datetime import date
from unittest.mock import MagicMock
import pytest

from app.agent.detect import detect_node
from app.agent.recommend import recommend_node
from app.agent.respond import respond_node
from app.agent.graph import compiled_graph


# -------------------------------------------------------------
# 1. Detection Logic Tests
# -------------------------------------------------------------
def test_detect_high_usage_threshold():
    """Test that a customer with high usage is loaded properly."""
    mock_customer = MagicMock()
    mock_customer.id = 1
    mock_customer.name = "Sara"
    mock_customer.current_plan = "5GB Data Plan"
    mock_customer.usage_percentage = 95.0
    mock_customer.contract_end_date = date(2026, 12, 31)

    mock_db = MagicMock()
    mock_db.query().filter().first.return_value = mock_customer

    initial_state = {
        "customer_id": 1,
        "message": "My internet is slow",
        "_db": mock_db,
    }

    result = detect_node(initial_state)

    assert result.get("customer_data") is not None
    assert result["customer_data"]["name"] == "Sara"


def test_detect_missing_customer():
    """Test detect node sets customer_data to None when ID does not exist."""
    mock_db = MagicMock()
    mock_db.query().filter().first.return_value = None

    initial_state = {
        "customer_id": 99999,
        "message": "Hello",
        "_db": mock_db,
    }

    result = detect_node(initial_state)
    assert result.get("customer_data") is None


# -------------------------------------------------------------
# 2. Recommendation Engine Logic Tests
# -------------------------------------------------------------
def test_recommend_upgrade_for_high_usage():
    """Test recommendation generation when trigger_reason is high usage."""
    state = {
        "customer_data": {
            "name": "Sara",
            "current_plan": "5GB Data Plan",
            "usage_percentage": 95.0,
        },
        "trigger_reason": "high_usage",
        "intent": {"needs": "more_data"},
    }

    result = recommend_node(state)
    recommendation = result.get("recommendation")

    assert recommendation is not None
    assert "primary" in recommendation


# -------------------------------------------------------------
# 3. Response Generation Formatting Tests
# -------------------------------------------------------------
def test_respond_node_structure():
    """Test that respond node parses dict offer and outputs response text."""
    state = {
        "customer_data": {
            "name": "Sara",
            "current_plan": "5GB Data Plan",
            "usage_percentage": 95.0,
        },
        "recommendation": {
            "primary": {
                "name": "100GB Premium Plan",
                "price": 45,
            }
        },
        "action": "offer",
        "trigger_reason": "high_usage",
    }

    result = respond_node(state)
    assert "response" in result
    assert isinstance(result["response"], str)
    assert len(result["response"]) > 0


# -------------------------------------------------------------
# 4. Full Graph Run
# -------------------------------------------------------------
def test_full_graph_run():
    """Test compiled graph invocation with complete mocked data."""
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

    initial_state = {
        "customer_id": 1,
        "message": "I keep running out of data.",
        "_db": mock_db,
    }

    result = compiled_graph.invoke(initial_state)
    assert result["response"] != ""
    assert result.get("action") is not None