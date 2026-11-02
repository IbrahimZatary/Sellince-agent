from app.agent.recommend import recommend_node
from app.agent.respond import respond_node
from app.agent.understand import _keyword_classify


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


def test_bilingual_keyword_classification():
    """Test bilingual and dialect classification (Arabic, Jordanian slang, Arabizi)."""
    # Jordanian slang acceptance
    res1 = _keyword_classify("يلا اعتمد بدي اشترك بالفايبر")
    assert res1["intent"] == "accepts_offer"

    # Arabizi acceptance
    res2 = _keyword_classify("bdi ashtrek bl offer")
    assert res2["intent"] == "accepts_offer"

    # Arabic price objection
    res3 = _keyword_classify("السعر كثير غالي ما بقدر ادفع")
    assert res3["intent"] == "objection"
    assert res3["objection_type"] == "price"

    # Arabic negation / disinterest
    res4 = _keyword_classify("بديش مش مهتم شكرا")
    assert res4["intent"] == "objection"

    # Arabic inquiry for details
    res5 = _keyword_classify("ممكن تفاصيل اكثر عن العرض وسرعة النت؟")
    assert res5["intent"] == "wants_details"

    # Arabic ready to pay
    res6 = _keyword_classify("ابعثلي رابط الدفع بدي ادفع هسا")
    assert res6["intent"] == "ready_to_pay"