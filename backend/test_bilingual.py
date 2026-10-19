import requests

BASE_URL = "http://127.0.0.1:8000/api/chat"

test_cases = [
    {"name": "Pure English Close", "payload": {"customer_id": 101, "message": "I want the fiber bundle, let's do it"}},
    {"name": "Jordanian Slang Close", "payload": {"customer_id": 102, "message": "يلا اعتمد بدي اشترك بالفايبر"}},
    {"name": "Arabizi / Franco", "payload": {"customer_id": 103, "message": "bdi ashtrek bl fiber yzm"}},
    {"name": "Formal MSA Hesitation", "payload": {"customer_id": 104, "message": "أريد معرفة المزيد من التفاصيل من فضلك"}},
    {"name": "Mixed Language Rejection", "payload": {"customer_id": 105, "message": "بديش الغي ال deal"}}
]

print("Starting Bilingual Stress Test...\n" + "="*40)
for case in test_cases:
    print(f"Testing: {case['name']}")
    print(f"User   : {case['payload']['message']}")
    try:
        response = requests.post(BASE_URL, json=case['payload'])
        data = response.json()
        print(f"Agent  : {data.get('response')}")
        print(f"Action : {data.get('action_payload')}")
    except Exception as e:
        print("Error: Could not connect. Make sure uvicorn app.main:app is running in another terminal.")
    print("-" * 40)
