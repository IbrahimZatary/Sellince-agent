from agent_state import AgentState

from app.rag.customer_recommendation import recommend_product_for_customer


def recommend_node(state: AgentState) -> AgentState:
    if state["customer_data"] is None:
        state["recommendation"] = None
        return state

    # In a multi-turn conversation, keep the existing recommendation
    # unless we explicitly decide to replace it later.
    existing_recommendation = state.get("recommendation")
    if existing_recommendation:
        return state

    customer_data = state["customer_data"]

    class CustomerContext:
        def __init__(self, data: dict):
            self.usage_percentage = data["usage_percentage"]
            self.segment = data.get("segment")

    customer_context = CustomerContext(customer_data)

    primary = recommend_product_for_customer(customer_context)

    state["recommendation"] = {
        "primary": primary,
        "alternative": None,
    }

    return state