import json
import os
from app.agent.agent_state import AgentState

def recommend_node(state: AgentState) -> AgentState:
    customer = state.get("customer_data") or {}
    usage = customer.get("usage_percentage", 85)
    
    # Load products catalog
    products_path = os.path.join(os.path.dirname(__file__), "products.json")
    products = []
    
    if os.path.exists(products_path):
        try:
            with open(products_path, "r", encoding="utf-8") as f:
                products = json.load(f)
        except Exception:
            products = []
            
    # Fallback products if json doesn't exist
    if not products:
        products = [
            {"id": "fiber_mobile_bundle", "name": "Fiber + Mobile Bundle", "price": 45, "description": "High-speed fiber paired with mobile data"},
            {"id": "speed_boost", "name": "Speed Boost 100Mbps", "price": 25, "description": "Extra speed add-on for heavy usage"}
        ]
        
    # Select recommendation based on usage
    selected_offer = products[0]
    for p in products:
        if usage > 80 and ("bundle" in p.get("id", "").lower() or "fiber" in p.get("name", "").lower()):
            selected_offer = p
            break
            
    state["recommendation"] = selected_offer
    state["offer"] = selected_offer
    return state
