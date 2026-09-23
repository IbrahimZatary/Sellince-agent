from typing import Optional


def determine_conversation_stage(
    intent: dict,
    previous_stage: Optional[str] = None,
) -> Optional[str]:
    intent_type = intent.get("intent")

    # First message:
    # Start with ENGAGE unless the customer's intent
    # already clearly belongs to a later stage.
    if previous_stage is None:
        initial_stage_map = {
            "wants_details": "EXPLAIN_OFFER",
            "objection": "HANDLE_OBJECTION",
            "accepts_offer": "CLOSE_DEAL",
            "ready_to_pay": "ROUTE_TO_PAYMENT",
            "other": "ENGAGE",
        }

        return initial_stage_map.get(
            intent_type,
            "ENGAGE",
        )

    # Continue the existing conversation based
    # on the new customer intent.
    transitions = {
        "ENGAGE": {
            "wants_details": "EXPLAIN_OFFER",
            "objection": "HANDLE_OBJECTION",
            "accepts_offer": "CLOSE_DEAL",
            "ready_to_pay": "ROUTE_TO_PAYMENT",
            "other": "ENGAGE",
        },
        "EXPLAIN_OFFER": {
            "objection": "HANDLE_OBJECTION",
            "accepts_offer": "CLOSE_DEAL",
            "ready_to_pay": "ROUTE_TO_PAYMENT",
            "wants_details": "EXPLAIN_OFFER",
        },
        "HANDLE_OBJECTION": {
            "objection": "HANDLE_OBJECTION",
            "accepts_offer": "CLOSE_DEAL",
            "ready_to_pay": "ROUTE_TO_PAYMENT",
            "wants_details": "EXPLAIN_OFFER",
        },
        "CLOSE_DEAL": {
            "objection": "HANDLE_OBJECTION",
            "ready_to_pay": "ROUTE_TO_PAYMENT",
            "accepts_offer": "CLOSE_DEAL",
        },
        "ROUTE_TO_PAYMENT": {
            "ready_to_pay": "ROUTE_TO_PAYMENT",
        },
    }

    return transitions.get(
        previous_stage,
        {},
    ).get(
        intent_type,
        previous_stage,
    )