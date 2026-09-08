from datetime import date, timedelta
from unittest.mock import MagicMock
import pytest
from app.agent.graph import compiled_graph
from app.agent.detect import check_triggers

# ---------------------------------------------------------------------
# 1. Test Trigger Rules against trigger_rules.md
# ---------------------------------------------------------------------
def test_rule_1_high_usage():
    customer = {
        "usage_percentage": 92,
        "contract_end_date": "2026-12-31",
        "current_plan": "20GB Data Plan",
        "segment": "Heavy User",
    }
    assert check_triggers(customer) == "high_data_usage"


def test_rule_2_contract_expiring():
    expiring_date = (date.today() + timedelta(days=15)).strftime("%Y-%m-%d")
    customer = {
        "usage_percentage": 45,
        "contract_end_date": expiring_date,
        "current_plan": "10GB Data Plan",
        "segment": "Average User",
    }
    assert check_triggers(customer) == "contract_expiring"


def test_rule_3_prepaid_heavy_user():
    customer = {
        "usage_percentage": 15,
        "contract_end_date": None,
        "current_plan": "Prepaid Plan",
        "segment": "Heavy User",
    }
    assert check_triggers(customer) == "prepaid_heavy_user"


# ---------------------------------------------------------------------
# 2. Test E2E Graph Output against api_contract.md format
# ---------------------------------------------------------------------
def test_api_contract_format_and_keys():
    mock_customer = MagicMock()
    mock_customer.id = 1
    mock_customer.name = "Ahmed Al-Fayez"
    mock_customer.phone = "0791111111"
    mock_customer.current_plan = "20GB Data Plan"
    mock_customer.usage_percentage = 92.0
    mock_customer.contract_end_date = date(2026, 12, 31)
    mock_customer.segment = "Heavy User"

    mock_db = MagicMock()
    mock_db.query.return_value.filter.return_value.first.return_value = mock_customer

    initial_state = {
        "customer_id": 1,
        "message": "I need more data",
        "_db": mock_db,
    }

    result = compiled_graph.invoke(initial_state)

    # Check api_contract.md keys
    assert "response" in result, "Missing 'response' in result"
    assert "action" in result, "Missing 'action' in result"
    assert result["action"] in ["show_offer", "ask_question", "escalate"], (
        f"Invalid action: {result.get('action')}"
    )

    if result.get("action") == "show_offer":
        offer = result.get("offer") or result.get("recommendation", {}).get("primary")
        assert offer is not None, "Missing offer payload"
        # Verify offer keys match api_contract.md
        assert "product" in offer or "name" in offer
        assert "price" in offer
        assert "description" in offer