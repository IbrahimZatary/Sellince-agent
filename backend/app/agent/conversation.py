from typing import Optional


def determine_conversation_stage(intent: dict) -> Optional[str]:
    intent_type = intent.get("intent")

    stage_map = {
        "wants_details": "EXPLAIN_OFFER",
        "objection": "HANDLE_OBJECTION",
        "accepts_offer": "CLOSE_DEAL",
        "ready_to_pay": "ROUTE_TO_PAYMENT",
    }

    return stage_map.get(intent_type)