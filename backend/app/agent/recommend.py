import json
from pathlib import Path

from app.agent.agent_state import AgentState
from app.rag.config import CHROMA_DIR, PRODUCTS_FILE
from app.rag.customer_recommendation import (
    get_upgrade_candidates,
    recommend_product_for_customer,
)


def _infer_service_type(current_plan: str) -> str | None:
    """Infer the customer's service type from their plan name when unset."""
    plan = (current_plan or "").strip().lower()
    if "fiber" in plan:
        return "fiber_home"
    if "gb" in plan or "mobile" in plan:
        return "mobile_data"
    return None


class _CustomerContext:
    """Thin adapter so customer_recommendation can be called from the graph."""

    def __init__(self, data: dict):
        current_plan = data.get("current_plan") or ""
        self.service_type = data.get("service_type") or _infer_service_type(current_plan)
        self.usage_percentage = data.get("usage_percentage", 0) or 0.0
        self.current_plan = current_plan
        self.speed = data.get("speed")
        self.segment = data.get("segment")
        self.interests = data.get("interests")
        self.location = data.get("location")


def _get_products_for_upgrade(ctx: _CustomerContext) -> list[dict]:
    """Get eligible upgrade products based on customer context and service type."""
    with PRODUCTS_FILE.open(encoding="utf-8") as handle:
        products = json.load(handle)

    service_type = ctx.service_type or "mobile_data"
    segment = (ctx.segment or "").strip().lower()

    # Determine target segment based on customer
    if segment == "heavy user":
        target_segments = ["Heavy User", "Families"]
    elif segment == "average user":
        target_segments = ["Average User", "Families"]
    elif segment == "low user":
        target_segments = ["Low User", "Average User", "Families"]
    else:
        target_segments = ["Heavy User", "Average User", "Low User", "Families", "Mobile Users"]

    # Filter products by service type and target segment
    eligible = []
    for product in products:
        if product["type"] != ctx.service_type:
            continue
        if product.get("target_segment") in target_segments:
            eligible.append(product)

    return eligible


def _select_product_for_upgrade(ctx: _CustomerContext) -> dict | None:
    """Select the best upgrade product for the customer."""
    eligible = []
    for product in _get_products_for_upgrade(ctx):
        eligible.append(product)

    if not eligible:
        return None

    # Sort by price ascending, prefer next tier up
    eligible.sort(key=lambda p: p["price"])
    return eligible[0] if eligible else None


def _select_product_for_postpaid_switch(ctx: _CustomerContext) -> dict | None:
    """Select postpaid plan for prepaid user wanting to switch."""
    with PRODUCTS_FILE.open(encoding="utf-8") as handle:
        products = json.load(handle)

    # Postpaid mobile data plans (not prepaid, not add-ons, not fiber, not bundles)
    postpaid_plans = [
        p for p in products
        if p["type"] == "mobile_data"
        and p["name"] not in ("5G Add-on",)
    ]

    if not postpaid_plans:
        return None

    # Sort by price, recommend the entry-level postpaid plan
    postpaid_plans.sort(key=lambda p: p["price"])
    return postpaid_plans[0] if postpaid_plans else None


def _select_recommendation(customer_data: dict, search_type: str) -> dict | None:
    """Select recommendation based on search type."""
    if search_type == "data_upgrade":
        ctx = _CustomerContext(customer_data)
        product = _select_product_for_upgrade(_CustomerContext(customer_data))
    elif search_type == "postpaid_switch":
        product = _select_product_for_postpaid_switch(_CustomerContext(customer_data))
    else:
        return None

    if not product:
        return None

    return {
        "product_id": product["product_id"],
        "product_name": product["name"],
        "type": product["type"],
        "speed": product["speed"],
        "price": product["price"],
        "description": product["description"],
        "features": product["features"],
        "target_segment": product["target_segment"],
    }


def recommend_node(state: AgentState) -> AgentState:
    """Stage 3: RECOMMEND Node.

    Recommends a real product for the customer using the rule-based recommender
    (+ RAG retrieval when the vector store exists). In a multi-turn conversation
    the existing recommendation is kept, unless it was never computed, so the
    offer stays stable across stages.

    Logic matches Kareem's branch exactly:
    - high_data_usage, contract_expiring, or usage >= 90% → data upgrade
    - prepaid_heavy_user → postpaid switch
    - intent needs: "plan upgrade", "more data", "upgrade" → data upgrade
    - else → no offer
    """
    trigger = state.get("trigger_reason")

    if trigger == "customer_not_found" or not state.get("customer_data"):
        state["recommendation"] = {"primary": None, "alternative": None}
        state["action"] = "ask_question"
        return state

    # In a multi-turn conversation, keep the existing recommendation
    existing_recommendation = state.get("recommendation")
    if existing_recommendation and existing_recommendation.get("primary"):
        return state

    customer = state.get("customer_data") or {}
    usage = float(customer.get("usage_percentage") or 0.0)
    intent = state.get("intent") or {}
    needs = intent.get("needs") or []
    trigger = state.get("trigger_reason")

    # Kareem's logic: explicit per-trigger handling
    search_type = None

    if trigger in ("high_data_usage", "contract_expiring") or usage >= 90:
        search_type = "data_upgrade"
    elif trigger == "prepaid_heavy_user":
        search_type = "postpaid_switch"
    elif any(n in ("plan upgrade", "more data", "upgrade") for n in needs):
        search_type = "data_upgrade"
    else:
        state["recommendation"] = {"primary": None, "alternative": None}
        state["action"] = "ask_question"
        return state

    # Select product based on search type
    primary = None
    if CHROMA_DIR.exists():
        try:
            # Try RAG first with customer context
            ctx = _CustomerContext(state.get("customer_data") or {})
            primary = recommend_product_for_customer(ctx) or None
        except Exception as exc:
            print(f"[Recommend] RAG retrieval unavailable for this request: {exc}")
            primary = None

    if not primary:
        # Fallback to our custom product selection
        if "postpaid" in search_type:
            primary = _select_product_for_postpaid_switch(_CustomerContext(state.get("customer_data") or {}))
        else:
            # data_upgrade
            ctx = _CustomerContext(state.get("customer_data") or {})
            primary = _select_product_for_upgrade(_CustomerContext(state.get("customer_data") or {}))

    state["recommendation"] = {"primary": primary, "alternative": None}
    state["action"] = "show_offer" if primary else "ask_question"
    return state