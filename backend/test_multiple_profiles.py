import requests
import time

API_URL = "http://127.0.0.1:8000/api/chat"

# Note: Adjust customer_ids 15 and 16 if your mock database uses different IDs 
# for travelers or device upgrade profiles.
scenarios = [
    {
        "name": "Scenario 1: Nadia - Heavy Data User (Fiber Lag)",
        "customer_id": 14,
        "messages": [
            "hello",
            "Yes, what options do you have for my data usage?",
            "let's do it"
        ]
    },
    {
        "name": "Scenario 2: Ahmed - Frequent Traveler (Roaming Pass)",
        "customer_id": 15,
        "messages": [
            "Hi, I'm traveling to Europe next week.",
            "What kind of roaming packages do you recommend?",
            "Sign me up."
        ]
    },
    {
        "name": "Scenario 3: Sarah - Low Usage / Device Upgrade",
        "customer_id": 16,
        "messages": [
            "Hey there, my current phone is getting really slow.",
            "Tell me more about the upgrade options.",
            "Okay, let's proceed."
        ]
    }
]

print("=== RUNNING MULTI-USE-CASE FASTAPI TESTS ===\n")

for scenario in scenarios:
    print(f"?? STARTING: {scenario['name']}")
    customer_id = scenario["customer_id"]
    
    for i, msg in enumerate(scenario["messages"], 1):
        payload = {"customer_id": customer_id, "message": msg}
        print(f"\n[Turn {i}] User (ID {customer_id}): '{msg}'")
        
        try:
            response = requests.post(API_URL, json=payload)
            if response.status_code == 200:
                data = response.json()
                print(f"?? Bot Response: {data.get('response', '')}")
                
                payload_data = data.get("offer") or data.get("action_payload")
                if payload_data and i == 3:
                    print(f"?? Payload Generated: {data.get('action_payload')}")
            else:
                print(f"? Error {response.status_code}: {response.text}")
        except Exception as e:
            print(f"? Connection failed. Is FastAPI running? Error: {e}")
            
        time.sleep(1) # Slight pause to let the backend breathe
        
    print("\n" + "="*50 + "\n")

print("=== ALL SCENARIOS COMPLETE ===")
