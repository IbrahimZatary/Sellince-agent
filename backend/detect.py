from datetime import datetime, timedelta

from agent_state import AgentState
from app.core.database import SessionLocal
from app.models.customer import Customer


def check_triggers(customer: dict) -> str | None:
    if customer["usage_percentage"] >= 90:
        return "high_data_usage"

    end_date = customer.get("contract_end_date")

    if end_date:
        end = datetime.strptime(end_date, "%Y-%m-%d")

        if end - datetime.now() < timedelta(days=30):
            return "contract_expiring"

    if (
        customer["segment"] == "Heavy User"
        and customer["current_plan"] == "Prepaid Plan"
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
        }

        state["trigger_reason"] = check_triggers(
            state["customer_data"]
        )

        return state

    finally:
        db.close()