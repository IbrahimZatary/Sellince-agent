from datetime import date

from agent_state import AgentState
from app.core.database import SessionLocal
from app.models.customer import Customer
from app.rag.customer_recommendation import UPGRADE_RULES


def check_triggers(customer: dict) -> list[str]:
    triggers = []

    service_type = customer.get("service_type")
    rule = UPGRADE_RULES.get(service_type)

    # Mobile usage >= 90%, Fiber usage >= 85%.
    if rule and customer["usage_percentage"] >= rule["threshold"]:
        if service_type == "mobile_data":
            triggers.append("high_data_usage")
        else:
            triggers.append("high_fiber_usage")

    # 5G offer:
    # Mobile customer + interested in 5G + not already on 5G.
    if service_type == "mobile_data":
        interests = customer.get("interests") or ""
        current_plan = customer.get("current_plan") or ""
        current_speed = customer.get("speed") or ""

        interested_in_5g = "5G" in interests.upper()
        already_on_5g = (
            "5G" in current_plan.upper()
            or current_speed.upper() == "5G"
        )

        if interested_in_5g and not already_on_5g:
            triggers.append("5g_interest")

    # Retention:
    # Contract expires in less than 30 days.
    end_date = customer.get("contract_end_date")

    if end_date:
        days_remaining = (
            date.fromisoformat(end_date) - date.today()
        ).days

        if 0 <= days_remaining < 30:
            triggers.append("contract_expiring")

    # Preserve the existing prepaid trigger.
    if (
        customer.get("segment") == "Heavy User"
        and customer.get("current_plan") == "PrepaidPlan"
    ):
        triggers.append("prepaid_heavy_user")

    return triggers


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
            state["trigger_reasons"] = ["customer_not_found"]
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

        state["trigger_reasons"] = check_triggers(
            state["customer_data"]
        )

        return state

    finally:
        db.close()