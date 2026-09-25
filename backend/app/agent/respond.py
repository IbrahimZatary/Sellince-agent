import os
from dotenv import load_dotenv
from groq import Groq
from app.agent.agent_state import AgentState

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_NAME = "openai/gpt-oss-20b"

def respond_node(state: AgentState) -> AgentState:
    customer_id = state.get("customer_id")
    customer = state.get("customer_data") or {}
    customer_name = customer.get("name", "there")
    current_plan = customer.get("current_plan", "Standard Plan")
    usage_pct = customer.get("usage_percentage", 0)
    
    user_message = state.get("message", "")
    user_msg_lower = user_message.lower().strip()
    history = state.get("history") or []

    history_text = " ".join([msg.get("content", "").lower() for msg in history[-4:] if isinstance(msg, dict)])
    context_text = user_msg_lower + " " + history_text

    if any(w in context_text for w in ["travel", "europe", "roaming", "trip", "rome"]):
        offer = {
            "id": "eu_roaming_pass",
            "name": "Europe Roaming Pass",
            "price": 15,
            "description": "10GB of high-speed roaming data across Europe for 14 days."
        }
    elif any(w in context_text for w in ["phone", "device", "upgrade", "hardware", "slow"]):
        offer = {
            "id": "device_upgrade_promo",
            "name": "Device Upgrade Promo",
            "price": 25,
            "description": "Upgrade to the latest flagship smartphone with 0% financing and a trade-in bonus."
        }
    else:
        offer = {
            "id": "fiber_mobile_bundle",
            "name": "Fiber + Mobile Bundle",
            "price": 45,
            "description": "High-speed home fiber paired with mobile data plan to prevent throttling."
        }
    
    # NEW FIX: Context Bleed Prevention
    last_offer_id = state.get("last_offer_id")
    if last_offer_id and last_offer_id != offer["id"]:
        # Offer changed! Clear the short-term history to prevent hallucinating old products
        history = []
    
    # Save the current offer ID for the next turn
    state["last_offer_id"] = offer["id"]
    
    state["offer"] = offer
    prod_name = offer.get("name", "our premium plan")
    prod_price = offer.get("price", "standard rate")
    prod_desc = offer.get("description", "A great new addition to your account.")
    current_stage = state.get("sales_stage", "engage")

    is_greeting = any(kw == user_msg_lower for kw in ["hello", "hi", "hey", "good morning", "good afternoon"])
    
    strong_close_keywords = ["let's do it", "lets do it", "sign me up", "proceed", "buy", "purchase", "get it", "add it", "run it", "connect me", "i want it", "link", "route me"]
    soft_close_keywords = ["yes", "sure", "ok", "okay", "deal", "sounds good", "right", "trust you"]
    negation_keywords = ["no ", "not ", "wait", "should i", "is it", "what", "?", "hesitant", "nevermind", "nvm", "don't want", "dont want", "help", "sorry", "my bad", "tell me", "more", "offers", "details"]

    has_strong_close = any(kw in user_msg_lower for kw in strong_close_keywords)
    has_soft_close = any(kw in user_msg_lower for kw in soft_close_keywords)
    has_negation = any(kw in user_msg_lower for kw in negation_keywords)

    if has_strong_close or (has_soft_close and not has_negation):
        next_stage = "close"
        action = "route_checkout"
    elif has_negation:
        next_stage = "explain"
        action = "show_offer"
    elif current_stage == "engage":
        next_stage = "engage" if is_greeting else "explain"
        action = "show_offer" if not is_greeting else "chat"
    else:
        next_stage = "explain"
        action = "show_offer"

    state["sales_stage"] = next_stage
    state["action"] = action

    system_prompt = f"""You are a warm, highly empathetic telecom sales advisor chatting with {customer_name}.
Customer Context:
- Current Plan: {current_plan}
- Data Usage: {usage_pct}%

Pitched Offer: {prod_name} for {prod_price} JOD
Offer Details: {prod_desc}
Current Stage: {next_stage.upper()}

Strict Behavioral Rules by Stage:
- If Stage is ENGAGE: Greet them gently. DO NOT pitch the product name or price yet!
- If Stage is EXPLAIN: Patiently answer any questions they have. If they are hesitant, validate their concerns gently. Explain the {prod_name} without being pushy. 
- If Stage is CLOSE: Express authentic excitement, celebrate their choice, and state you are routing them to checkout.
- Keep responses warm, conversational, and complete (2-3 sentences max)."""

    response_text = ""
    is_blocked_by_safety = False
    
    try:
        client = Groq(api_key=GROQ_API_KEY)
        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "system", "content": system_prompt}, *history[-4:], {"role": "user", "content": user_message}],
            temperature=0.3,
            max_tokens=1024
        )
        choice = completion.choices[0]
        if hasattr(choice, "message") and hasattr(choice.message, "content"):
            response_text = choice.message.content.strip()
            
            if "sorry, but i can" in response_text.lower() or "cannot fulfill" in response_text.lower():
                is_blocked_by_safety = True
    except Exception as e:
        print(f"[Groq API Notice]: Using fallback due to: {e}")
        is_blocked_by_safety = True

    if is_blocked_by_safety:
        response_text = "I'm here to help with your telecom needs, but let's keep our chat professional. How can I assist you with your account today?"
        state["action_payload"] = None
        history.append({"role": "user", "content": "[Message removed due to safety guidelines]"})
        history.append({"role": "assistant", "content": response_text})
    else:
        if not response_text:
            response_text = "I'm here to help! Let me pull up the best options for your account."

        if action == "route_checkout" or next_stage == "close":
            prod_id = offer.get("id") or str(prod_name).lower().replace(" ", "_").replace("+", "")
            state["action_payload"] = {
                "label": "Continue to Purchase",
                "url": f"/checkout?customer_id={customer_id}&agent_id=45&product_id={prod_id}"
            }
        else:
            state["action_payload"] = None

        history.append({"role": "user", "content": user_message})
        history.append({"role": "assistant", "content": response_text})
        
    state["response"] = response_text
    state["history"] = history

    return state
