import json
from pathlib import Path

from app.agent.agent_state import AgentState
from app.rag.config import CHROMA_DIR, PRODUCTS_FILE
from app.rag.customer_recommendation import (
    get_upgrade_candidates,
    recommend_product_for_customer,
)

OFFERING_TRIGGERS = ("high_data_usage", "contract_expiring", "prepaid_heavy_user")


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


def _catalog_fallback(ctx: _CustomerContext) -> dict | None:
    """Pick the next larger eligible product straight from products.json.

    Used when the Chroma vector store is not built yet, so /chat keeps working
    with zero setup. Mirrors customer_recommendation.recommend_product_for_customer
    without touching the retriever.
    """
    product_type, eligible_ids = get_upgrade_candidates(ctx)
    if not eligible_ids:
        return None

    with PRODUCTS_FILE.open(encoding="utf-8") as handle:
        products = json.load(handle)

    match = next(
        (product for product in products if product["product_id"] in eligible_ids),
        None,
    )
    if match is None:
        return None

    return {
        "product_id": match["product_id"],
        "product_name": match["name"],
        "type": match["type"],
        "speed": match["speed"],
        "price": match["price"],
        "description": match["description"],
        "features": match["features"],
        "target_segment": match["target_segment"],
    }


def recommend_node(state: AgentState) -> AgentState:
    """Stage 3: RECOMMEND Node.

    Recommends a real product for the customer using the rule-based recommender
    (+ RAG retrieval when the vector store exists). Keeps the previous action
    contract: show_offer when a recommendation exists, else ask_question.
    """
    trigger = state.get("trigger_reason")

    if trigger == "customer_not_found":
        state["recommendation"] = {"primary": None, "alternative": None}
        state["action"] = "ask_question"
        return state

    customer = state.get("customer_data") or {}
    intent = state.get("intent") or {}
    needs = intent.get("needs") or []
    usage = float(customer.get("usage_percentage") or 0.0)

    wants_offer = (
        trigger in OFFERING_TRIGGERS
        or usage >= 90
        or any(need in ("plan upgrade", "more data", "upgrade") for need in needs)
    )

    if not wants_offer or not customer:
        state["recommendation"] = {"primary": None, "alternative": None}
        state["action"] = "ask_question"
        return state

    ctx = _CustomerContext(customer)

    primary = None
    if CHROMA_DIR.exists():
        try:
            primary = recommend_product_for_customer(ctx) or None
        except Exception as exc:  # noqa: BLE001 - vector store may be unavailable
            print(f"[Recommend] RAG retrieval unavailable for this request: {exc}")
            primary = None

    if not primary:
        primary = _catalog_fallback(ctx)

    state["recommendation"] = {"primary": primary, "alternative": None}
    state["action"] = "show_offer" if primary else "ask_question"
    return state