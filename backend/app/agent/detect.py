from datetime import date, datetime

from app.agent.agent_state import AgentState
from app.core.database import SessionLocal
from app.models.customer import Customer
from app.rag.customer_recommendation import UPGRADE_RULES


def check_triggers(customer: dict) -> str | None:
    service_type = customer.get("service_type")
    rule = UPGRADE_RULES.get(service_type)

    # 1. Mobile usage >= 90%, Fiber usage >= 85%.
    usage = float(customer.get("usage_percentage") or 0)
    if rule and usage >= rule["threshold"]:
        return (
            "high_data_usage"
            if service_type == "mobile_data"
            else "high_fiber_usage"
        )

    # 2. Contracts ending today or within the next 29 days.
    end_date = customer.get("contract_end_date")
    if end_date:
        try:
            d = (
                end_date
                if isinstance(end_date, date)
                else date.fromisoformat(str(end_date))
            )
            days_remaining = (d - date.today()).days
            if 0 <= days_remaining < 30:
                return "contract_expiring"
        except (ValueError, TypeError):
            pass

    # 3. Preserve the existing prepaid trigger.
    if (
        customer.get("segment") == "Heavy User"
        and customer.get("current_plan") == "Prepaid Plan"
    ):
        return "prepaid_heavy_user"

    # 4. 5G Interest Offer
    interests = str(customer.get("interests") or "").lower()
    if service_type == "mobile_data" and "5g" in interests:
        return "5g_offer"

    # 5. Fiber Cross-Sell
    location = str(customer.get("location") or "").lower()
    fiber_eligible_areas = [
        "amman",
        "abdoun",
        "sweifieh",
        "khalda",
        "jabal amman",
    ]
    if service_type == "mobile_data" and location and any(
        area in location for area in fiber_eligible_areas
    ):
        return "fiber_cross_sell"

    return None


def detect_node(state: AgentState) -> AgentState:
    customer_id = state.get("customer_id")
    if customer_id is None:
        state["customer_data"] = None
        state["trigger_reason"] = "customer_not_found"
        return state

    db = SessionLocal()

    try:
        row = (
            db.query(Customer)
            .filter(Customer.id == customer_id)
            .first()
        )

        if row is None:
            state["customer_data"] = None
            state["trigger_reason"] = "customer_not_found"
            return state

        customer_data = {
            "customer_id": row.id,
            "name": row.name,
            "phone": row.phone,
            "current_plan": row.current_plan,
            "usage_percentage": float(row.usage_percentage or 0),
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

        state["customer_data"] = customer_data
        state["trigger_reason"] = check_triggers(customer_data)

        return state

    finally:
        db.close()
