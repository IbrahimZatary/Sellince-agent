import json
import os
from agent_state import AgentState

try:
    from groq import Groq
except ImportError:
    Groq = None

_GROQ_CLIENT = None

def _get_client():
    global _GROQ_CLIENT
    if _GROQ_CLIENT is None and Groq:
        api_key = os.getenv("GROQ_API_KEY")
        if api_key:
            _GROQ_CLIENT = Groq(api_key=api_key)
    return _GROQ_CLIENT


def respond_node(state: AgentState) -> AgentState:
    """Stage 4: RESPOND Node powered by Groq.
    Generates personalized pitch, structured offer, and next action.
    """
    customer = state.get("customer_data")
    recommendation = state.get("recommendation") or {}
    trigger = state.get("trigger_reason")
    primary_offer = recommendation.get("primary")
    message = state.get("message") or ""
    client = _get_client()

    customer_name = customer["name"] if customer else "valued customer"
    current_plan = customer.get("current_plan", "current plan") if customer else ""
    usage = int(customer.get("usage_percentage", 0)) if customer else 0

    if trigger == "customer_not_found" or not customer:
        state["response"] = "Customer profile could not be found. How can I assist you today?"
        state["offer"] = None
        state["action"] = "ask_question"
        return state

    if not primary_offer:
        state["response"] = f"Hi {customer_name}, how can I help you today with your plan?"
        state["offer"] = None
        state["action"] = "ask_question"
        return state

    offer_name = (
        primary_offer.get("product")
        or primary_offer.get("product_name")
        or primary_offer.get("name")
        or "recommended plan"
    )
    offer_price = primary_offer.get("price", "")
    offer_desc = primary_offer.get("description", "")

    # Attempt LLM pitch generation with Groq
    if client:
        try:
            system_prompt = (
                "You are an expert, professional sales AI for a telecom provider. "
                "Craft a concise (1-2 sentences max), highly personalized message to the customer. "
                f"Refer to the customer by name ({customer_name}), mention their current plan or usage ({usage}% on {current_plan}), "
                f"and pitch the recommended offer: {offer_name} for {offer_price} JOD. "
                "Be direct, polite, and persuasive without being pushy."
            )
            user_prompt = f"Customer trigger: {trigger}. Customer asked/said: '{message}'."

            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.3,
                max_tokens=120,
            )
            llm_text = completion.choices[0].message.content.strip()
            state["response"] = llm_text
            state["offer"] = {
                "product": offer_name,
                "price": offer_price,
                "description": offer_desc,
            }
            state["action"] = "show_offer"
            return state
        except Exception as e:
            print(f"[Groq Respond] Falling back to rule-based template: {e}")

    # Fallback to deterministic message templates
    if trigger == "high_data_usage":
        msg = (
            f"Hi {customer_name}, I see you're using {usage}% of your {current_plan}. "
            f"We have a {offer_name} for just {offer_price} JOD. Interested?"
        )
    elif trigger == "contract_expiring":
        msg = (
            f"Hi {customer_name}, your contract for {current_plan} is expiring soon. "
            f"We have an exclusive offer on the {offer_name} for {offer_price} JOD to keep you connected."
        )
    elif trigger == "prepaid_heavy_user":
        msg = (
            f"Hi {customer_name}, we noticed your high data usage on {current_plan}. "
            f"You could get better value with our {offer_name} for {offer_price} JOD."
        )
    else:
        price_text = f" for {offer_price} JOD" if offer_price else ""
        msg = f"Hi {customer_name}, we recommend upgrading to the {offer_name}{price_text}."

    state["response"] = msg
    state["offer"] = {
        "product": offer_name,
        "price": offer_price,
        "description": offer_desc,
    }
    state["action"] = "show_offer"
    return state
