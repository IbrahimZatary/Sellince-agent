from agent_state import AgentState

from app.agent.templates import (
    initial_engagement_template,
    explain_offer_template,
    close_and_route_template,
)
from app.rag.response_generator import generate_stage_response


MOCK_PRODUCT_PAGE_URL = "/mock/product"


def respond_node(state: AgentState) -> AgentState:
    customer = state.get("customer_data")
    recommendation = state.get("recommendation") or {}
    stage = state.get("conversation_stage")

    primary_offer = recommendation.get("primary", {})

    customer_name = (
        customer["name"]
        if customer
        else "valued customer"
    )

    if state.get("trigger_reason") == "customer_not_found":
        state["response"] = "Customer profile could not be found."
        state["action"] = "abort"
        return state

    if not primary_offer:
        state["response"] = (
            f"Hello {customer_name}, thank you for reaching out. "
            f"How can we assist you with your account today?"
        )
        state["action"] = "general_response"
        return state

    product_name = primary_offer.get(
        "product_name",
        "our recommended package",
    )
    price = primary_offer.get("price")
    features = primary_offer.get("features", [])
    target_segment = primary_offer.get(
        "target_segment",
        "customers",
    )

    if stage == "ENGAGE":
        state["response"] = initial_engagement_template(
            customer_name=customer_name,
            usage_percentage=customer.get("usage_percentage"),
            current_plan=customer.get("current_plan"),
            product_name=product_name,
            price=price,
        )

        state["action"] = "offer_presented"
        return state

    if stage == "EXPLAIN_OFFER":
        state["response"] = explain_offer_template(
            product_name=product_name,
            feature_1=_get_feature(features, 0),
            feature_2=_get_feature(features, 1),
            feature_3=_get_feature(features, 2),
            target_segment=target_segment,
        )

        state["action"] = "offer_explained"
        return state

    if stage == "HANDLE_OBJECTION":
        customer_context = {
            "customer_name": customer_name,
            "current_plan": customer.get("current_plan"),
            "usage_percentage": customer.get("usage_percentage"),
            "segment": customer.get("segment"),
        }

        state["response"] = generate_stage_response(
            stage=stage,
            customer_context=customer_context,
            product_info=primary_offer,
            customer_message=state["message"],
        )

        state["action"] = "objection_handled"
        return state

    if stage == "CLOSE_DEAL":
        state["response"] = close_and_route_template(
            product_name=product_name,
            feature_1=_get_feature(features, 0),
            feature_2=_get_feature(features, 1),
            feature_3=_get_feature(features, 2),
            product_page_url=MOCK_PRODUCT_PAGE_URL,
        )

        state["action"] = "deal_closed"
        return state

    if stage == "ROUTE_TO_PAYMENT":
        state["response"] = (
            f"You can continue to the payment step for the "
            f"{product_name}."
        )

        state["action"] = "route_to_payment"
        return state

    # No stage yet = initial engagement
    state["response"] = initial_engagement_template(
        customer_name=customer_name,
        usage_percentage=customer.get("usage_percentage"),
        current_plan=customer.get("current_plan"),
        product_name=product_name,
        price=price,
    )

    state["action"] = "offer_presented"

    return state


def _get_feature(features: list, index: int) -> str:
    if index < len(features):
        return str(features[index])

    return "Feature information unavailable"