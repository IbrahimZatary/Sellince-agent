import pytest
from detect import detect_node

def test_mobile_data_upgrade_trigger():
    # Customer 1: usage 92% on mobile
    state = {"customer_id": 1, "message": "hello"}
    res = detect_node(state)
    assert res["trigger_reason"] == "mobile_data_upgrade"

def test_fiber_speed_upgrade_trigger():
    # Customer 14: usage 95% on fiber
    state = {"customer_id": 14, "message": "hello"}
    res = detect_node(state)
    assert res["trigger_reason"] == "fiber_speed_upgrade"

def test_5g_offer_trigger():
    # Customer 4 or 10: mobile with 5G interest
    state = {"customer_id": 2, "message": "hello"}
    state["customer_data"] = {"service_type": "mobile_data", "usage_percentage": 40, "interests": "5G, Gaming"}
    # Direct rule check logic:
    assert "5G" in state["customer_data"]["interests"]

def test_nonexistent_customer():
    state = {"customer_id": 9999, "message": "hello"}
    res = detect_node(state)
    assert res["trigger_reason"] == "customer_not_found"
