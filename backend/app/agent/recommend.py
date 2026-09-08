from app.agent.agent_state import AgentState

PRODUCTS_CATALOG = [
    {
        "product": "50GB Data Plan",
        "price": 25,
        "description": "50GB data with 5G speed and unlimited calls",
    },
    {
        "product": "Entertainment Pack",
        "price": 5,
        "description": "Unlimited streaming on selected video and music apps",
    },
    {
        "product": "Postpaid Smart Plan",
        "price": 20,
        "description": "30GB data, 1000 local minutes, and postpaid perks",
    },
]


def search_products(query: str) -> dict:
    """Mock RAG product search. Replaceable by ChromaDB retrieval."""
    query_lower = (query or "").lower()
    if "prepaid" in query_lower or "postpaid" in query_lower:
        return {
            "primary": PRODUCTS_CATALOG[2],
            "alternative": PRODUCTS_CATALOG[0],
        }
    return {
        "primary": PRODUCTS_CATALOG[0],
        "alternative": PRODUCTS_CATALOG[1],
    }


def recommend_node(state: AgentState) -> AgentState:
    """Stage 3: RECOMMEND Node."""
    trigger = state.get("trigger_reason")
    customer = state.get("customer_data") or {}
    intent = state.get("intent") or {}
    needs = intent.get("needs") or []
    usage = float(customer.get("usage_percentage") or 0.0)

    # Check trigger reasons, customer usage directly, or intent needs
    if trigger in ["high_data_usage", "contract_expiring"] or usage >= 90:
        recs = search_products("data_upgrade")
        state["recommendation"] = recs
        state["action"] = "show_offer"
    elif trigger == "prepaid_heavy_user":
        recs = search_products("postpaid_switch")
        state["recommendation"] = recs
        state["action"] = "show_offer"
    elif any(n in ["plan upgrade", "more data", "upgrade"] for n in needs):
        recs = search_products("data_upgrade")
        state["recommendation"] = recs
        state["action"] = "show_offer"
    else:
        state["recommendation"] = None
        state["action"] = "ask_question"

    return state