from decimal import Decimal
import re

from app.agent.agent_state import AgentState
from app.rag.customer_recommendation import (
    UPGRADE_RULES,
    recommend_product_for_customer,
)
from app.rag.retriever import search_products


def recommend_node(state: AgentState) -> AgentState:
    """Stage 3: RECOMMEND Node.

    Recommends a real product for the customer using RAG retrieval.
    In a multi-turn conversation the existing recommendation is kept,
    unless it was never computed, so the offer stays stable across stages.
    """
    trigger = state.get("trigger_reason")

    if trigger == "customer_not_found" or not state.get("customer_data"):
        state["recommendation"] = {"primary": None, "alternative": None}
        state["offer"] = None
        state["action"] = "ask_question"
        return state

    customer = state.get("customer_data") or {}

    # Check proactive active offer first
    active_offer = state.get("active_offer")
    if isinstance(active_offer, dict) and (
        active_offer.get("product_name") or active_offer.get("name")
    ):
        state["recommendation"] = {"primary": active_offer, "alternative": None}
        state["offer"] = active_offer
        state["action"] = "show_offer"
        return state

    # In a multi-turn conversation, keep the existing recommendation FIRST
    existing_recommendation = state.get("recommendation")
    if existing_recommendation and isinstance(existing_recommendation, dict):
        primary = existing_recommendation.get("primary", existing_recommendation)
        if isinstance(primary, dict) and primary.get("product_name"):
            # Invalidate if customer already has this plan (e.g. after checkout)
            current_plan = customer.get("current_plan", "").strip().lower()
            recommended_plan = primary.get("product_name", "").strip().lower()
            if current_plan and recommended_plan and current_plan == recommended_plan:
                state["recommendation"] = {"primary": None, "alternative": None}
                state["offer"] = None
            else:
                state["recommendation"] = {"primary": primary, "alternative": None}
                state["offer"] = primary
                state["action"] = "show_offer"
                return state

    usage = float(customer.get("usage_percentage") or 0.0)
    intent = state.get("intent") or {}
    needs = intent.get("needs") or []

    # Per-trigger handling (supporting both original and proactive trigger names)
    search_type = None

    sales_triggers = (
        "high_data_usage",
        "mobile_data_upgrade",
        "high_fiber_usage",
        "fiber_speed_upgrade",
        "contract_expiring",
        "retention_offer",
        "5g_offer",
        "fiber_cross_sell",
    )

    if trigger in sales_triggers or usage >= 90:
        search_type = "data_upgrade"
    elif trigger in ("prepaid_heavy_user", "postpaid_switch"):
        search_type = "postpaid_switch"
    elif any(n in ("plan upgrade", "more data", "upgrade") for n in needs):
        search_type = "data_upgrade"
    elif any(
        w in (state.get("message") or "").lower()
        for w in ("upgrade", "more data", "plan upgrade", "change plan")
    ):
        search_type = "data_upgrade"
    else:
        state["recommendation"] = {"primary": None, "alternative": None}
        state["offer"] = None
        state["action"] = "ask_question"
        return state

    # Select product based on search type using RAG
    primary = None
    try:
        class CustomerContext:
            def __init__(self, data: dict):
                self.usage_percentage = data.get("usage_percentage", 0.0)
                self.segment = data.get("segment")
                self.current_plan = data.get("current_plan")
                self.service_type = data.get("service_type")
                self.speed = data.get("speed")
                self.interests = data.get("interests")
                self.location = data.get("location")

        customer_context = CustomerContext(customer)

        if search_type == "postpaid_switch":
            primary = search_products(
                query="postpaid mobile data plan",
                product_type="Mobile Data",
                eligible_product_ids=None,
            )
        elif search_type == "data_upgrade" and trigger in (
            "contract_expiring",
            "retention_offer",
        ):
            primary = _search_upgrade_products(customer_context)
        elif search_type == "data_upgrade" and trigger is None and any(
            w in (state.get("message") or "").lower()
            for w in ("upgrade", "more data", "plan upgrade", "change plan")
        ):
            primary = _search_upgrade_products(customer_context)
        else:
            primary = recommend_product_for_customer(customer_context)
    except Exception as exc:
        print(f"[Recommend] RAG retrieval unavailable: {exc}")
        primary = None

    if not primary:
        primary = None

    # Invalidate if recommended plan matches current plan
    if primary and primary.get("product_name"):
        current_plan = customer.get("current_plan", "").strip().lower()
        recommended_plan = primary.get("product_name", "").strip().lower()
        if current_plan and recommended_plan and current_plan == recommended_plan:
            primary = None

    state["recommendation"] = {"primary": primary, "alternative": None}
    state["offer"] = primary
    state["action"] = "show_offer" if primary else "ask_question"
    return state


def _extract_amount(value: str | None, unit: str) -> Decimal | None:
    if not value:
        return None
    match = re.search(
        rf"(\d+(?:\.\d+)?)\s*{re.escape(unit)}\b", value, flags=re.IGNORECASE
    )
    return Decimal(match.group(1)) if match else None


def _search_upgrade_products(ctx: "CustomerContext") -> dict | None:
    service_type = ctx.service_type
    rule = UPGRADE_RULES.get(service_type)
    if not rule:
        return None

    product_type = rule["product_type"]
    unit = rule["unit"]

    current_value = (
        ctx.current_plan if service_type == "mobile_data" else ctx.speed
    )
    current_amount = _extract_amount(current_value, unit)
    if current_amount is None:
        return None

    from app.rag.config import PRODUCTS_FILE
    import json

    with PRODUCTS_FILE.open("r", encoding="utf-8") as f:
        products = json.load(f)

    larger_products = []
    for product in products:
        if product["type"] != product_type:
            continue
        product_value = (
            product["name"]
            if service_type == "mobile_data"
            else product["speed"]
        )
        amount = _extract_amount(product_value, unit)
        if amount is not None and amount > current_amount:
            larger_products.append((amount, product))

    if not larger_products:
        return None

    larger_products.sort(key=lambda x: x[0])
    p = larger_products[0][1]
    return {
        "product_id": p["product_id"],
        "product_name": p["name"],
        "type": p["type"],
        "speed": p["speed"],
        "price": p["price"],
        "description": p["description"],
        "features": p["features"],
        "target_segment": p["target_segment"],
    }
