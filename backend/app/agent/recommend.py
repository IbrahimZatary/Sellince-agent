
from types import SimpleNamespace

from app.agent.agent_state import AgentState
from app.rag.customer_recommendation import (
    recommend_product_for_customer,
    UPGRADE_RULES,
)


def recommend_node(state: AgentState) -> AgentState:
    """
    Stage 3: RECOMMEND

    Uses Kareem's intent-based recommendation approach
    with the existing RAG product recommendation system.
    """

    customer = state.get("customer_data") or {}

    if not customer:
        state["recommendation"] = None
        state["offer"] = None
        return state

    # Keep an existing offer during multi-turn conversation.
    existing_offer = state.get("active_offer") or state.get("offer")

    if existing_offer:
        state["recommendation"] = existing_offer
        state["offer"] = existing_offer
        return state

    trigger = state.get("trigger_reason")
    intent_data = state.get("intent") or {}
    needs = intent_data.get("needs") or []

    needs_text = " ".join(str(item) for item in needs).lower()

    sales_keywords = (
        "upgrade",
        "more data",
        "plan",
        "offer",
        "purchase",
        "renew",
        "deal",
    )

    customer_requested_offer = any(
        keyword in needs_text for keyword in sales_keywords
    )

    sales_triggers = {
        "mobile_data_upgrade",
        "fiber_speed_upgrade",
        "retention_offer",
        "5g_offer",
        "fiber_cross_sell",
    }

    if not customer_requested_offer and trigger not in sales_triggers:
        state["recommendation"] = None
        state["offer"] = None
        return state

    service_type = customer.get("service_type")
    rule = UPGRADE_RULES.get(service_type)

    if not rule:
        state["recommendation"] = None
        state["offer"] = None
        return state

    # Adapt PostgreSQL customer data to the existing
    # RAG recommendation function's expected attributes.
    customer_context = SimpleNamespace(
        service_type=service_type,
        current_plan=customer.get("current_plan") or "",
        speed=customer.get("speed"),
        usage_percentage=float(
            customer.get("usage_percentage") or 0
        ),
        segment=customer.get("segment"),
        interests=customer.get("interests"),
        location=customer.get("location"),
    )

    try:
        offer = recommend_product_for_customer(customer_context)
    except Exception as exc:
        print(f"[Recommend] RAG retrieval failed: {exc}")
        offer = None

    if not offer:
        state["recommendation"] = None
        state["offer"] = None
        return state

    # Prevent recommending the customer's current plan.
    current_plan = (
        customer.get("current_plan") or ""
    ).strip().lower()

    recommended_plan = (
        offer.get("product_name") or offer.get("name") or ""
    ).strip().lower()

    if current_plan and recommended_plan == current_plan:
        state["recommendation"] = None
        state["offer"] = None
        return state

    # Kareem's responder expects a direct product dictionary.
    state["recommendation"] = offer
    state["offer"] = offer

    return state
