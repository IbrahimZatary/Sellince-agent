import os

from app.agent.agent_state import AgentState
from app.agent.templates import initial_engagement_template

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

    Generates a personalized pitch, a structured offer, and the next action.
    Falls back to deterministic templates (initial_engagement_template) when
    Groq is unreachable, keeping responses grounded in the real catalog.
    """
    customer = state.get("customer_data") or {}
    recommendation = state.get("recommendation") or {}
    trigger = state.get("trigger_reason")
    primary_offer = recommendation.get("primary")
    message = state.get("message") or ""
    client = _get_client()

    customer_name = customer.get("name") or "valued customer"
    current_plan = customer.get("current_plan") or ""
    usage = int(customer.get("usage_percentage") or 0)
    service_type = customer.get("service_type")

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
        primary_offer.get("product_name")
        or primary_offer.get("name")
        or primary_offer.get("product")
        or "recommended plan"
    )
    offer_price = primary_offer.get("price", "")
    offer_desc = primary_offer.get("description", "")
    features = primary_offer.get("features") or []

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
    state["response"] = initial_engagement_template(
        customer_name=customer_name,
        usage_percentage=usage,
        current_plan=current_plan,
        product_name=offer_name,
        price=offer_price,
        service_type=service_type,
    )
    state["offer"] = {
        "product": offer_name,
        "price": offer_price,
        "description": offer_desc,
    }
    state["action"] = "show_offer"
    return state