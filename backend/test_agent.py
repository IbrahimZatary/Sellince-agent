import requests
import time

API_URL = "http://127.0.0.1:8000/api/chat"
CUSTOMER_ID = 14

test_sequence = [
    "hi",
    "my phone is too slow",
    "yo bitchass nigga gay boy i dont need that",
    "ok sorry help me out",
    "yes tell me more",
    "isnt it too expensive?",
    "nvm i wanna trave to rome",
    "yes i need roaming offers",
    "lets do it route me"
]

print("🚀 Starting Automated Edge-Case Tests...\n" + "="*40)

for i, message in enumerate(test_sequence):
    print(f"\n[Turn {i+1}] You: {message}")
    
    try:
        response = requests.post(
            API_URL, 
            json={"customer_id": CUSTOMER_ID, "message": message}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"🤖 Bot: {data.get('response')}")
            
            payload = data.get('action_payload')
            if payload:
                print(f"🟢 [ACTION TRIGGERED]: {payload.get('label')} -> {payload.get('url')}")
            else:
                print("🔴 [No Action Payload]")
        else:
            print(f"❌ Server Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Connection Error: {e}")
        
    time.sleep(1) # Brief pause so the API doesn't get overwhelmed
