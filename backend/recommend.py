from agent_state import AgentState
from app.rag.customer_recommendation import (
    recommend_products_for_customer,
)


def remove_duplicate_recommendations(
    recommendations: list[dict],
) -> list[dict]:
    """
    Remove duplicate catalog products while preserving
    the original recommendation order.

    If multiple triggers produce the same product,
    the product is presented only once.
    """

    unique_recommendations = []
    seen_product_ids = set()

    for recommendation in recommendations:
        product_id = recommendation.get(
            "product_id"
        )

        # Non-product recommendations, such as
        # retention opportunities, do not have a
        # product_id and should be preserved.
        if product_id is None:
            unique_recommendations.append(
                recommendation
            )
            continue

        if product_id in seen_product_ids:
            continue

        seen_product_ids.add(product_id)
        unique_recommendations.append(
            recommendation
        )

    return unique_recommendations


def recommend_node(
    state: AgentState,
) -> AgentState:
    if state["customer_data"] is None:
        state["recommendation"] = None
        return state

    customer_data = state["customer_data"]

    trigger_reasons = (
        state.get("trigger_reasons") or []
    )

    class CustomerContext:
        def __init__(self, data: dict):
            self.usage_percentage = (
                data["usage_percentage"]
            )
            self.segment = data.get(
                "segment"
            )
            self.current_plan = data.get(
                "current_plan"
            )
            self.service_type = data.get(
                "service_type"
            )
            self.speed = data.get(
                "speed"
            )
            self.interests = data.get(
                "interests"
            )
            self.location = data.get(
                "location"
            )
            self.contract_end_date = data.get(
                "contract_end_date"
            )

    customer_context = CustomerContext(
        customer_data
    )

    recommendations = (
        recommend_products_for_customer(
            customer=customer_context,
            trigger_reasons=trigger_reasons,
        )
    )

    recommendations = (
        remove_duplicate_recommendations(
            recommendations
        )
    )

    primary = (
        recommendations[0]
        if recommendations
        else {}
    )

    alternative = (
        recommendations[1]
        if len(recommendations) > 1
        else None
    )

    state["recommendation"] = {
        "primary": primary,
        "alternative": alternative,
        "all": recommendations,
    }

    return state