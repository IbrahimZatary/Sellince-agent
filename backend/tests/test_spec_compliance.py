from datetime import date, timedelta

from app.agent.detect import check_triggers


# ---------------------------------------------------------------------
# 1. Trigger Rules (Manar's detect logic)
# ---------------------------------------------------------------------
def test_rule_1_high_usage():
    customer = {
        "service_type": "mobile_data",
        "usage_percentage": 92,
        "contract_end_date": "2026-12-31",
        "current_plan": "20GB Data Plan",
        "segment": "Heavy User",
    }
    assert check_triggers(customer) == "high_data_usage"


def test_rule_2_contract_expiring():
    expiring_date = (date.today() + timedelta(days=15)).strftime("%Y-%m-%d")
    customer = {
        "usage_percentage": 45,
        "contract_end_date": expiring_date,
        "current_plan": "10GB Data Plan",
        "segment": "Average User",
    }
    assert check_triggers(customer) == "contract_expiring"


def test_rule_3_prepaid_heavy_user():
    customer = {
        "usage_percentage": 15,
        "contract_end_date": None,
        "current_plan": "Prepaid Plan",
        "segment": "Heavy User",
    }
    assert check_triggers(customer) == "prepaid_heavy_user"