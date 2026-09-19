from app.agent.recommend import recommend_node
from app.agent.respond import respond_node


def test_recommend_upgrade_for_high_usage():
    """Test recommendation generation when a customer is loaded."""
    state = {
        "customer_data": {
            "name": "Sara",
            "current_plan": "5GB Data Plan",
            "usage_percentage": 95.0,
        },
    }

    result = recommend_node(state)
    recommendation = result.get("recommendation")

    assert recommendation is not None
    assert "primary" in recommendation


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
    }

    result = respond_node(state)
    assert "response" in result
    assert isinstance(result["response"], str)
    assert len(result["response"]) > 0