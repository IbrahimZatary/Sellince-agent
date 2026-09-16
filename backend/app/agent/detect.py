from datetime import date, datetime

from app.agent.agent_state import AgentState
from app.models.customer import Customer
from app.rag.customer_recommendation import UPGRADE_RULES
from app.core.database import SessionLocal


def _text(value) -> str | None:
    return value if isinstance(value, str) and value.strip() else None


def check_triggers(customer: dict) -> str | None:
    service_type = customer.get("service_type")
    rule = UPGRADE_RULES.get(service_type)
    usage = customer.get("usage_percentage") or 0.0

    # Mobile usage >= 90%, Fiber usage >= 85%.
    if rule and usage >= rule["threshold"]:
        return (
            "high_data_usage"
            if service_type == "mobile_data"
            else "high_fiber_usage"
        )

    # Unset service type still signals high data usage above 90%.
    if not rule and usage >= 90:
        return "high_data_usage"

    # Contracts ending today or within the next 29 days.
    end_date = customer.get("contract_end_date")
    if end_date:
        if isinstance(end_date, str):
            end_dt = date.fromisoformat(end_date)
        elif isinstance(end_date, datetime):
            end_dt = end_date.date()
        elif isinstance(end_date, date):
            end_dt = end_date
        else:
            end_dt = None

        if end_dt:
            days_remaining = (end_dt - date.today()).days
            if 0 <= days_remaining < 30:
                return "contract_expiring"

    # Preserve the existing prepaid trigger.
    segment = (customer.get("segment") or "").strip().lower()
    plan = (customer.get("current_plan") or "").strip().lower()

    if segment == "heavy user" and plan == "prepaid plan":
        return "prepaid_heavy_user"

    return None


def detect_node(state: AgentState) -> AgentState:
    db = state.get("_db") or SessionLocal()
    owns_db = state.get("_db") is None

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
            "usage_percentage": float(row.usage_percentage) if row.usage_percentage is not None else 0.0,
            "contract_end_date": (
                row.contract_end_date.isoformat()
                if row.contract_end_date
                else None
            ),
            "segment": row.segment,
            "service_type": _text(getattr(row, "service_type", None)),
            "speed": _text(getattr(row, "speed", None)),
            "interests": _text(getattr(row, "interests", None)),
            "location": _text(getattr(row, "location", None)),
        }

        state["trigger_reason"] = check_triggers(
            state["customer_data"]
        )

        return state

    finally:
        if owns_db:
            db.close()