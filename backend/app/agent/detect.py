from datetime import datetime
import json
from pathlib import Path
from app.agent.agent_state import AgentState

CUSTOMER_DB_PATH = Path(__file__).resolve().parent / "mock_customers.json"


def load_customers():
    if not CUSTOMER_DB_PATH.exists():
        return {}
    with open(CUSTOMER_DB_PATH, "r", encoding="utf-8-sig") as f:
        data = json.load(f)
    return {c["customer_id"]: c for c in data}


def detect_node(state: AgentState) -> AgentState:
    """Stage 1: DETECT Node
    Identifies triggers based on customer profile, usage, contract, and interests.
    """
    customer_id = state.get("customer_id")
    customers = load_customers()
    customer = customers.get(customer_id)

    if not customer:
        state["customer_data"] = None
        state["trigger_reason"] = "customer_not_found"
        return state

    state["customer_data"] = customer

    # 1. Retention Check (< 30 days remaining)
    contract_end = customer.get("contract_end_date")
    if contract_end:
        try:
            end_date = datetime.strptime(contract_end, "%Y-%m-%d").date()
            days_left = (end_date - datetime.now().date()).days
            if 0 <= days_left < 30:
                state["trigger_reason"] = "retention_offer"
                return state
        except ValueError:
            pass

    service_type = customer.get("service_type")
    usage = customer.get("usage_percentage", 0)
    interests = str(customer.get("interests") or "")
    location = customer.get("location")

    # 2. Mobile Data Upgrade (usage >= 90%)
    if service_type == "mobile_data" and usage >= 90:
        state["trigger_reason"] = "mobile_data_upgrade"
        return state

    # 3. Fiber Speed Upgrade (usage >= 85%)
    if service_type == "fiber_home" and usage >= 85:
        state["trigger_reason"] = "fiber_speed_upgrade"
        return state

    # 4. 5G Interest Offer
    if service_type == "mobile_data" and "5G" in interests:
        state["trigger_reason"] = "5g_offer"
        return state

    # 5. Fiber Cross-Sell
    # If location is known, match coverage areas; if location is None, target steady mobile accounts without home internet
    fiber_eligible_areas = ["amman", "abdoun", "sweifieh", "khalda", "jabal amman"]
    if service_type == "mobile_data":
        if location and any(area in location.lower() for area in fiber_eligible_areas):
            state["trigger_reason"] = "fiber_cross_sell"
            return state
        elif not location and 30 <= usage < 80:
            state["trigger_reason"] = "fiber_cross_sell"
            return state

    state["trigger_reason"] = "general_inquiry"
    return state
