from types import SimpleNamespace

import pytest

from app.agent.recommend import recommend_node
from app.rag import customer_recommendation

MOCK_CUSTOMER = {
    "name": "Dana",
    "current_plan": "20GB Mobile 4G",
    "usage_percentage": 95.0,
    "service_type": "mobile_data",
    "speed": None,
    "segment": "Heavy User",
    "interests": "streaming",
    "location": "Amman",
}


def _ctx(**overrides):
    base = {
        "service_type": "mobile_data",
        "usage_percentage": 95.0,
        "current_plan": "20GB Mobile 4G",
        "speed": None,
        "segment": "Heavy User",
        "interests": "more data",
        "location": "Amman",
    }
    base.update(overrides)
    return SimpleNamespace(**base)


def test_upgrade_candidates_mobile_high_usage():
    ptype, ids = customer_recommendation.get_upgrade_candidates(_ctx())
    assert ptype == "Mobile Data"
    assert ids == [1]


def test_upgrade_candidates_mobile_low_usage():
    ptype, ids = customer_recommendation.get_upgrade_candidates(
        _ctx(usage_percentage=50, interests=None)
    )
    assert ptype == "Mobile Data"
    assert ids == []


def test_upgrade_candidates_fiber_by_speed():
    ptype, ids = customer_recommendation.get_upgrade_candidates(
        _ctx(service_type="fiber_home", speed="50 Mbps", current_plan="Fiber 50 Mbps")
    )
    assert ptype == "Fiber Home"
    assert ids == [4]


@pytest.mark.skip(reason="needs a built Chroma store and embedding model")
def test_recommend_node_uses_rag():
    state = {
        "customer_data": dict(MOCK_CUSTOMER),
        "trigger_reason": "high_data_usage",
        "intent": {"needs": ["more data"]},
    }
    result = recommend_node(state)
    primary = result["recommendation"]["primary"]
    assert result["action"] == "show_offer"
    assert primary and primary["product_name"] == "50GB Mobile 5G"


def test_recommend_node_catalog_fallback():
    state = {
        "customer_data": dict(MOCK_CUSTOMER),
        "trigger_reason": "high_data_usage",
        "intent": {"needs": ["more data"]},
    }
    result = recommend_node(state)
    primary = result["recommendation"]["primary"]
    assert result["action"] == "show_offer"
    assert primary is not None
    assert primary["product_name"] == "50GB Mobile 5G"
    assert primary["price"] == 25


def test_recommend_node_low_usage_asks_question():
    state = {
        "customer_data": {
            **MOCK_CUSTOMER,
            "usage_percentage": 40.0,
        },
        "trigger_reason": None,
        "intent": {"needs": ["billing question"]},
    }
    result = recommend_node(state)
    assert result["action"] == "ask_question"
    assert result["recommendation"]["primary"] is None


def test_recommend_node_missing_customer():
    state = {
        "customer_data": {},
        "trigger_reason": "customer_not_found",
        "intent": {},
    }
    result = recommend_node(state)
    assert result["action"] == "ask_question"
    assert result["recommendation"]["primary"] is None


def test_recommend_node_empty_eligible_catalog():
    state = {
        "customer_data": {
            **MOCK_CUSTOMER,
            "service_type": "unknown_type",
            "current_plan": "5GB Mobile 4G",
            "usage_percentage": 95.0,
        },
        "trigger_reason": "high_data_usage",
        "intent": {"needs": []},
    }
    result = recommend_node(state)
    assert result["action"] == "ask_question"
    assert result["recommendation"]["primary"] is None