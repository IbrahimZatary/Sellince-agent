from app.agent.agent_state import AgentState


def respond_node(state: AgentState) -> AgentState:
    customer = state.get("customer_data")
    intent = state.get("intent") or {}
    recommendation = state.get("recommendation") or {}

    primary_offer = recommendation.get("primary", {})
    offer_name = primary_offer.get("name", "our recommended package")
    offer_price = primary_offer.get("price", "")

    customer_name = customer["name"] if customer else "valued customer"

    if state.get("trigger_reason") == "customer_not_found":
        state["response"] = "Customer profile could not be found."
        state["action"] = "abort"
        return state

    # Formulate conversational response based on recommendation and intent
    if primary_offer:
        price_text = f" for only {offer_price} JOD" if offer_price else ""
        state["response"] = (
            f"Hello {customer_name}, based on your current usage patterns, "
            f"we recommend upgrading to the {offer_name}{price_text}. "
            f"Would you like us to activate this for you?"
        )
        state["action"] = "offer_presented"
    else:
        state["response"] = (
            f"Hello {customer_name}, thank you for reaching out. "
            f"How can we assist you with your account today?"
        )
        state["action"] = "general_response"

    return state