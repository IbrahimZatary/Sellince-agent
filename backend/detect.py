from datetime import date

from agent_state import AgentState
from app.core.database import SessionLocal
from app.models.customer import Customer
from app.rag.customer_recommendation import UPGRADE_RULES


def check_triggers(customer: dict) -> str | None:
    service_type = customer.get("service_type")
    rule = UPGRADE_RULES.get(service_type)

    # Mobile usage >= 90%, Fiber usage >= 85%.
    if rule and customer["usage_percentage"] >= rule["threshold"]:
        return (
            "high_data_usage"
            if service_type == "mobile_data"
            else "high_fiber_usage"
        )

    # Contracts ending today or within the next 29 days.
    end_date = customer.get("contract_end_date")

    if end_date:
        days_remaining = (
            date.fromisoformat(end_date) - date.today()
        ).days

        if 0 <= days_remaining < 30:
            return "contract_expiring"

    # Preserve the existing prepaid trigger.
    if (
        customer.get("segment") == "Heavy User"
        and customer.get("current_plan") == "Prepaid Plan"
    ):
        return "prepaid_heavy_user"

    return None


def detect_node(state: AgentState) -> AgentState:
    db = SessionLocal()

    try:
        row = (
            db.query(Customer)
            .filter(Customer.id == state["customer_id"])
            .first()
        )

        if row is None:
            state["customer_data"] = None
            state["trigger_reason"] = "customer_not_found"
            return state

        state["customer_data"] = {
            "name": row.name,
            "phone": row.phone,
            "current_plan": row.current_plan,
            "usage_percentage": float(row.usage_percentage),
            "contract_end_date": (
                row.contract_end_date.isoformat()
                if row.contract_end_date
                else None
            ),
            "segment": row.segment,
            "service_type": row.service_type,
            "speed": row.speed,
            "interests": row.interests,
            "location": row.location,
        }

        state["trigger_reason"] = check_triggers(
            state["customer_data"]
        )

        return state

    finally:
        db.close()