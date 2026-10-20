
from datetime import date, datetime

from app.agent.agent_state import AgentState
from app.core.database import SessionLocal
from app.models.customer import Customer


def check_triggers(customer: dict) -> str:
    """
    Detect sales opportunities using Kareem's rules.
    Customer information comes from PostgreSQL.
    """

    # 1. Retention Check
    contract_end = customer.get("contract_end_date")

    if contract_end:
        try:
            end_date = (
                contract_end
                if isinstance(contract_end, date)
                else date.fromisoformat(str(contract_end))
            )

            days_left = (end_date - date.today()).days

            if 0 <= days_left < 30:
                return "retention_offer"

        except (ValueError, TypeError):
            pass

    service_type = customer.get("service_type")
    usage = float(customer.get("usage_percentage") or 0)
    interests = str(customer.get("interests") or "").lower()
    location = str(customer.get("location") or "").lower()

    # 2. Mobile Data Upgrade
    if service_type == "mobile_data" and usage >= 90:
        return "mobile_data_upgrade"

    # 3. Fiber Speed Upgrade
    if service_type == "fiber_home" and usage >= 85:
        return "fiber_speed_upgrade"

    # 4. 5G Interest Offer
    if service_type == "mobile_data" and "5g" in interests:
        return "5g_offer"

    # 5. Fiber Cross-Sell
    fiber_eligible_areas = [
        "amman",
        "abdoun",
        "sweifieh",
        "khalda",
        "jabal amman",
    ]

    if service_type == "mobile_data":
        if location and any(
            area in location for area in fiber_eligible_areas
        ):
            return "fiber_cross_sell"

        # Preserve Kareem's fallback for unknown locations.
        if not location and 30 <= usage < 80:
            return "fiber_cross_sell"

    return "general_inquiry"


def detect_node(state: AgentState) -> AgentState:
    """
    Stage 1: DETECT

    Loads customer data from PostgreSQL and applies
    Kareem's opportunity detection rules.
    """

    customer_id = state.get("customer_id")

    if customer_id is None:
        state["customer_data"] = None
        state["trigger_reason"] = "customer_not_found"
        return state

    db = SessionLocal()

    try:
        customer = (
            db.query(Customer)
            .filter(Customer.id == customer_id)
            .first()
        )

        if customer is None:
            state["customer_data"] = None
            state["trigger_reason"] = "customer_not_found"
            return state

        customer_data = {
            "customer_id": customer.id,
            "name": customer.name,
            "phone": customer.phone,
            "current_plan": customer.current_plan,
            "usage_percentage": float(
                customer.usage_percentage or 0
            ),
            "contract_end_date": (
                customer.contract_end_date.isoformat()
                if customer.contract_end_date
                else None
            ),
            "segment": customer.segment,
            "service_type": customer.service_type,
            "speed": customer.speed,
            "interests": customer.interests,
            "location": customer.location,
        }

        state["customer_data"] = customer_data
        state["trigger_reason"] = check_triggers(customer_data)

        return state

    finally:
        db.close()
