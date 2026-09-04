from app.agent.agent_state import AgentState

# STUB so the pipeline can be tested before Mariam's RAG module exists.
# Once she delivers it, delete this stub and replace with:
#   from mariam_rag import search_products
def search_products(query: str) -> dict:
    return {
        "product_name": "50GB Data Plan",
        "price": 25,
        "description": "50GB data with 5G speed and unlimited calls",
        "target_segment": "Heavy User",
    }


def recommend_node(state: AgentState) -> AgentState:
    if state["customer_data"] is None:
        state["recommendation"] = None
        return state

    intent = state.get("intent") or {}
    explicit_needs = intent.get("needs") if isinstance(intent, dict) else None

    should_recommend = bool(state["trigger_reason"]) or bool(explicit_needs)

    if not should_recommend:
        state["recommendation"] = None
        return state

    query = state["trigger_reason"] or (explicit_needs[0] if explicit_needs else state["customer_data"]["segment"])
    primary = search_products(query)
    state["recommendation"] = {"primary": primary, "alternative": None}
    return state