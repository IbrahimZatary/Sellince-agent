"""Proactive sessions now use the same decision path as a normal chat:

    detect -> recommend -> proactive (compose opener) -> END

These tests need no database or LLM: nodes and collaborators are faked.
"""

from types import SimpleNamespace

import pytest

from app.agent import graph as graph_module
from app.agent import proactive
from app.agent import recommend as recommend_module


OFFER = {
    "product_id": 1,
    "product_name": "50GB Mobile 5G",
    "price": 25,
}

CUSTOMER = {
    "customer_id": 19,
    "name": "Rania",
    "current_plan": "20GB Mobile Data",
    "usage_percentage": 97.0,
    "contract_end_date": "2026-11-05",
    "service_type": "mobile_data",
    "speed": "4G",
}


# ---------------------------------------------------------------- routers

def test_route_after_detect_message_path_is_unchanged():
    assert graph_module.route_after_detect(
        {"customer_data": CUSTOMER}
    ) == "understand"

    assert graph_module.route_after_detect(
        {"customer_data": None}
    ) == "respond"


def test_route_after_detect_proactive():
    assert graph_module.route_after_detect(
        {"entry_type": "proactive", "customer_data": CUSTOMER}
    ) == "recommend"

    assert graph_module.route_after_detect(
        {"entry_type": "proactive", "customer_data": None}
    ) == "end"


def test_route_after_recommend():
    assert graph_module.route_after_recommend(
        {"entry_type": "proactive"}
    ) == "proactive"

    assert graph_module.route_after_recommend({}) == "respond"
    assert graph_module.route_after_recommend(
        {"entry_type": "message"}
    ) == "respond"


# ------------------------------------------------------------ graph order

def _install_fake_nodes(monkeypatch, calls, *, customer=CUSTOMER, needs=None):
    def fake(name, update):
        def node(state):
            calls.append(name)
            return update
        return node

    monkeypatch.setattr(
        graph_module, "detect_node",
        fake("detect", {"customer_data": customer, "trigger_reason": "5g_offer"}),
    )
    monkeypatch.setattr(
        graph_module, "understand_node",
        fake("understand", {"intent": {"needs": needs or []}}),
    )
    monkeypatch.setattr(
        graph_module, "recommend_node", fake("recommend", {"offer": OFFER})
    )
    monkeypatch.setattr(
        graph_module, "respond_node", fake("respond", {"response": "reply"})
    )
    monkeypatch.setattr(
        graph_module, "proactive_offer_node",
        fake("proactive", {"response": "opener"}),
    )


def _run(initial):
    return graph_module.build_graph().compile().invoke(initial)


def test_proactive_session_runs_detect_recommend_proactive(monkeypatch):
    calls = []
    _install_fake_nodes(monkeypatch, calls)

    result = _run({"customer_id": 19, "entry_type": "proactive"})

    assert calls == ["detect", "recommend", "proactive"]
    assert result["response"] == "opener"


def test_proactive_session_with_unknown_customer_just_ends(monkeypatch):
    calls = []
    _install_fake_nodes(monkeypatch, calls, customer=None)

    _run({"customer_id": 999, "entry_type": "proactive"})

    assert calls == ["detect"]


def test_chat_without_sales_need_skips_recommend(monkeypatch):
    calls = []
    _install_fake_nodes(monkeypatch, calls)

    _run({"customer_id": 19, "message": "hello"})

    assert calls == ["detect", "understand", "respond"]


def test_chat_with_sales_need_goes_through_recommend(monkeypatch):
    calls = []
    _install_fake_nodes(monkeypatch, calls, needs=["plan upgrade"])

    _run({"customer_id": 19, "message": "I need an upgrade"})

    assert calls == ["detect", "understand", "recommend", "respond"]


# --------------------------------------------------------- proactive node

class _FakeQuery:
    def filter(self, *args, **kwargs):
        return self

    def scalar(self):
        return 7


class _FakeSession:
    def query(self, *args, **kwargs):
        return _FakeQuery()

    def close(self):
        pass


@pytest.fixture
def no_llm(monkeypatch):
    monkeypatch.setattr(proactive, "SessionLocal", lambda: _FakeSession())
    monkeypatch.setattr(proactive, "was_offer_recently_sent", lambda **kw: False)
    monkeypatch.setattr(proactive, "_get_client", lambda: None)


def _state(trigger="mobile_data_upgrade", offer=OFFER, **extra):
    return {
        "customer_id": 19,
        "entry_type": "proactive",
        "customer_data": CUSTOMER,
        "trigger_reason": trigger,
        "offer": offer,
        "recommendation": offer,
        **extra,
    }


def test_node_announces_the_offer_recommend_chose(no_llm):
    result = proactive.proactive_offer_node(_state())

    assert result["active_offer"] == OFFER
    assert result["recommendation"] == OFFER
    assert result["offer"] == OFFER
    assert result["conversation_stage"] == "ENGAGE"
    assert "Rania" in result["response"]
    assert "50GB Mobile 5G" in result["response"]
    assert "25 JOD" in result["response"]


@pytest.mark.parametrize(
    "trigger, fragment",
    [
        ("mobile_data_upgrade", "97% of your mobile data"),
        ("fiber_speed_upgrade", "97% of its speed capacity"),
        ("retention_offer", "2026-11-05"),
        ("5g_offer", "interest in 5G"),
        ("fiber_cross_sell", "home fiber"),
    ],
)
def test_opener_matches_the_trigger(no_llm, trigger, fragment):
    result = proactive.proactive_offer_node(_state(trigger=trigger))

    assert fragment in result["response"]


@pytest.mark.parametrize("offer", [None, {}, {"price": 10}])
def test_node_without_a_usable_offer_says_nothing(no_llm, offer):
    result = proactive.proactive_offer_node(
        _state(offer=offer, recommendation=offer)
    )

    assert result == {
        "active_offer": None,
        "recommendation": None,
        "offer": None,
        "response": None,
    }


def test_node_without_customer_says_nothing(no_llm):
    state = _state()
    state["customer_data"] = None

    assert proactive.proactive_offer_node(state)["response"] is None


def test_cooldown_suppresses_opener_and_clears_the_offer(
    monkeypatch, no_llm
):
    monkeypatch.setattr(proactive, "was_offer_recently_sent", lambda **kw: True)

    result = proactive.proactive_offer_node(_state())

    assert result["response"] is None
    # Not announced, so it must not stay in the checkpoint as "the offer".
    assert result["active_offer"] is None
    assert result["offer"] is None
    assert result["recommendation"] is None


def test_cooldown_check_uses_customer_company_and_product(
    monkeypatch, no_llm
):
    seen = {}

    def spy(**kwargs):
        seen.update(kwargs)
        return False

    monkeypatch.setattr(proactive, "was_offer_recently_sent", spy)

    proactive.proactive_offer_node(_state())

    assert seen["customer_id"] == 19
    assert seen["company_id"] == 7
    assert seen["product_name"] == "50GB Mobile 5G"


def _client(reply=None, error=None):
    captured = {}

    def create(**kwargs):
        captured.update(kwargs)

        if error:
            raise error

        message = SimpleNamespace(content=reply)
        return SimpleNamespace(choices=[SimpleNamespace(message=message)])

    client = SimpleNamespace(
        chat=SimpleNamespace(completions=SimpleNamespace(create=create))
    )
    return client, captured


def test_llm_opener_is_used_and_told_the_reason(monkeypatch, no_llm):
    client, captured = _client(reply="  Hello Rania!  ")
    monkeypatch.setattr(proactive, "_get_client", lambda: client)

    result = proactive.proactive_offer_node(_state())

    prompt = captured["messages"][0]["content"]

    assert result["response"] == "Hello Rania!"
    assert "97% of your mobile data" in prompt
    assert "50GB Mobile 5G" in prompt


@pytest.mark.parametrize("reply", ["", None, "   "])
def test_empty_llm_reply_falls_back(monkeypatch, no_llm, reply):
    client, _ = _client(reply=reply)
    monkeypatch.setattr(proactive, "_get_client", lambda: client)

    result = proactive.proactive_offer_node(_state())

    assert "50GB Mobile 5G" in result["response"]


def test_llm_failure_falls_back_instead_of_crashing(monkeypatch, no_llm):
    client, _ = _client(error=RuntimeError("groq down"))
    monkeypatch.setattr(proactive, "_get_client", lambda: client)

    result = proactive.proactive_offer_node(_state())

    assert result["active_offer"] == OFFER
    assert "50GB Mobile 5G" in result["response"]


# ------------------------------------- real recommend_node, real proactive

def test_real_recommend_node_feeds_the_proactive_node(monkeypatch, no_llm):
    """detect (faked: needs DB) -> REAL recommend -> REAL proactive."""
    monkeypatch.setattr(
        graph_module, "detect_node",
        lambda state: {
            "customer_data": CUSTOMER,
            "trigger_reason": "mobile_data_upgrade",
        },
    )
    monkeypatch.setattr(
        recommend_module, "recommend_product_for_customer",
        lambda customer: dict(OFFER),
    )

    result = _run({"customer_id": 19, "entry_type": "proactive"})

    assert result["active_offer"]["product_name"] == "50GB Mobile 5G"
    assert result["conversation_stage"] == "ENGAGE"
    assert "97% of your mobile data" in result["response"]


def test_trigger_without_a_product_produces_no_opener(monkeypatch, no_llm):
    monkeypatch.setattr(
        graph_module, "detect_node",
        lambda state: {
            "customer_data": CUSTOMER,
            "trigger_reason": "5g_offer",
        },
    )
    monkeypatch.setattr(
        recommend_module, "recommend_product_for_customer",
        lambda customer: {},
    )

    result = _run({"customer_id": 19, "entry_type": "proactive"})

    assert result.get("response") is None
    assert result.get("active_offer") is None