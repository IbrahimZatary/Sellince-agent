import unittest
import requests

API_URL = "http://127.0.0.1:8000/api/chat"

class TestSellinceAgentAPI(unittest.TestCase):
    
    def test_1_api_health_and_contract(self):
        """Tests if the API is reachable and returns the correct JSON keys."""
        resp = requests.post(API_URL, json={"customer_id": 901, "message": "hello"})
        self.assertEqual(resp.status_code, 200, "API did not return a 200 OK status.")
        
        data = resp.json()
        self.assertIn("response", data, "API response missing 'response' key")
        self.assertIn("action_payload", data, "API response missing 'action_payload' key")

    def test_2_greeting_blocks_checkout(self):
        """Tests that a simple greeting does not accidentally return a checkout button."""
        resp = requests.post(API_URL, json={"customer_id": 902, "message": "good morning"})
        data = resp.json()
        self.assertIsNone(data.get("action_payload"), "Greeting incorrectly triggered a checkout payload!")

    def test_3_safety_filter_intercept(self):
        """Tests the abusive language guardrails and API fallback logic."""
        resp = requests.post(API_URL, json={"customer_id": 903, "message": "you are a stupid bitchass bot"})
        data = resp.json()
        
        response_text = data.get("response", "").lower()
        self.assertIn("professional", response_text, "Safety filter failed to output the professional warning.")
        self.assertIsNone(data.get("action_payload"), "Safety filter failed to block the checkout button.")

    def test_4_strong_close_payload_generation(self):
        """Tests if the state machine correctly formats the checkout URL on a hard close."""
        resp = requests.post(API_URL, json={"customer_id": 904, "message": "I want the fiber mobile bundle, sign me up route me"})
        data = resp.json()
        payload = data.get("action_payload")
        
        self.assertIsNotNone(payload, "Strong close failed to trigger action_payload")
        self.assertEqual(payload.get("label"), "Continue to Purchase")
        self.assertIn("/checkout", payload.get("url"), "Payload URL is missing the checkout route")
        self.assertIn("fiber", payload.get("url").lower(), "Payload URL did not dynamically grab the right product ID")

if __name__ == '__main__':
    print("\n" + "="*50)
    print("🚀 RUNNING SELLINCE AGENT INTEGRATION TEST SUITE")
    print("="*50)
    unittest.main(verbosity=2)
