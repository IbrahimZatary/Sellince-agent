import sys
from fastapi.testclient import TestClient
from app.main import app

# Initialize FastAPI TestClient
client = TestClient(app)

print("=== RUNNING FULL E2E API & GRAPH TEST ===\n")

try:
    # ---------------------------------------------------------
    # TURN 1: Trigger the Pitch
    # ---------------------------------------------------------
    print("-> Turn 1: Customer triggers the bot ('My connection is slow')")
    r1 = client.post("/api/chat", json={"customer_id": 14, "message": "My connection is slow"})
    assert r1.status_code == 200, f"API Error: {r1.text}"
    d1 = r1.json()
    
    print(f"   Response: {d1.get('response')}")
    print(f"   Action: {d1.get('action')}")
    assert d1.get("action") == "show_offer", "Turn 1 failed to show offer."
    assert d1.get("action_payload") is None, "Payload should be None before closing."
    print("   [PASS] Turn 1\n")

    # ---------------------------------------------------------
    # TURN 2: Ask for Explanation (Memory Check)
    # ---------------------------------------------------------
    print("-> Turn 2: Customer asks for details ('Tell me more about the details')")
    r2 = client.post("/api/chat", json={"customer_id": 14, "message": "Tell me more about the details"})
    assert r2.status_code == 200, f"API Error: {r2.text}"
    d2 = r2.json()
    
    print(f"   Response: {d2.get('response')}")
    print(f"   Action: {d2.get('action')}")
    assert d2.get("action") == "show_offer", "Turn 2 failed to maintain 'show_offer' action."
    assert d2.get("offer") is not None, "Memory failed: Offer was lost."
    print("   [PASS] Turn 2\n")

    # ---------------------------------------------------------
    # TURN 3: Close and Route to Checkout
    # ---------------------------------------------------------
    print("-> Turn 3: Customer agrees ('Yes, let's do it')")
    r3 = client.post("/api/chat", json={"customer_id": 14, "message": "Yes, let's do it"})
    assert r3.status_code == 200, f"API Error: {r3.text}"
    d3 = r3.json()
    
    print(f"   Response: {d3.get('response')}")
    print(f"   Action: {d3.get('action')}")
    
    payload = d3.get("action_payload")
    print(f"   Payload: {payload}")
    
    assert d3.get("action") == "route_checkout", "Turn 3 failed to transition to 'route_checkout'."
    assert payload is not None, "Turn 3 failed to generate action_payload."
    assert "checkout?customer_id=14" in payload.get("url", ""), "Malformed checkout URL."
    print("   [PASS] Turn 3\n")

    print("=== ALL TESTS PASSED SUCCESSFULLY! ===")

except AssertionError as e:
    print(f"\n[X] TEST FAILED: {e}")
    sys.exit(1)
except Exception as e:
    print(f"\n[X] UNEXPECTED ERROR: {e}")
    sys.exit(1)
