from datetime import date, datetime, timedelta
from sqlalchemy.orm import Session

from agent_state import AgentState
from app.models.customer import Customer


def check_triggers(customer: dict) -> str | None:
    if not customer:
        return None

    usage = customer.get("usage_percentage") or 0.0
    if usage >= 90:
        return "high_data_usage"

    end_date = customer.get("contract_end_date")
    if end_date:
        if isinstance(end_date, str):
            try:
                end_dt = datetime.strptime(end_date[:10], "%Y-%m-%d").date()
            except ValueError:
                end_dt = None
        elif isinstance(end_date, (datetime, date)):
            end_dt = end_date.date() if isinstance(end_date, datetime) else end_date
        else:
            end_dt = None

        if end_dt and (end_dt - date.today()) < timedelta(days=30):
            return "contract_expiring"

    segment = (customer.get("segment") or "").strip().lower()
    plan = (customer.get("current_plan") or "").strip().lower()

    if "heavy" in segment and "prepaid" in plan:
        return "prepaid_heavy_user"

    return None


def detect_node(state: AgentState) -> AgentState:
    db: Session = state["_db"]
    row = db.query(Customer).filter(Customer.id == state["customer_id"]).first()

    if row is None:
        state["customer_data"] = None
        state["trigger_reason"] = "customer_not_found"
        return state

    state["customer_data"] = {
        "name": row.name,
        "phone": row.phone,
        "current_plan": row.current_plan,
        "usage_percentage": float(row.usage_percentage) if row.usage_percentage is not None else 0.0,
        "contract_end_date": row.contract_end_date.isoformat() if row.contract_end_date else None,
        "segment": row.segment,
    }
    state["trigger_reason"] = check_triggers(state["customer_data"])
    return state
