import os

from app.agent.agent_state import AgentState
from app.agent.templates import (
    initial_engagement_template,
    explain_offer_template,
    close_and_route_template,
)
from app.rag.response_generator import generate_stage_response

try:
    from groq import Groq
except ImportError:
    Groq = None


MOCK_PRODUCT_PAGE_URL = "/mock/product"

_GROQ_CLIENT = None


def _get_client():
    global _GROQ_CLIENT
    if _GROQ_CLIENT is None and Groq:
        api_key = os.getenv("GROQ_API_KEY")
        if api_key:
            _GROQ_CLIENT = Groq(api_key=api_key)
    return _GROQ_CLIENT


def _offer_name(primary_offer: dict) -> str:
    return (
        primary_offer.get("product_name")
        or primary_offer.get("name")
        or primary_offer.get("product")
        or "recommended plan"
    )


def _general_no_offer_response(customer_name: str) -> str:
    return (
        f"Hello {customer_name}, thank you for reaching out. "
        "How can we assist you with your account today?"
    )


def _engagement_response(
    message: str,
    trigger: str | None,
    customer_name: str,
    usage: int,
    current_plan: str,
    service_type: str | None,
    offer_name: str,
    offer_price,
) -> str:
    client = _get_client()
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
                # model="llama-3.3-70b-versatile",  # removed from Groq's API
                model=os.getenv("GROQ_MODEL", "openai/gpt-oss-20b"),  # app/rag/config.py
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.3,
                max_tokens=400,
            )
            return completion.choices[0].message.content.strip()
        except Exception as exc:  # noqa: BLE001 - Groq may be unavailable
            print(f"[Responses] Groq ENGAGE pitch failed, using template: {exc}")

    return initial_engagement_template(
        customer_name=customer_name,
        usage_percentage=usage,
        current_plan=current_plan,
        product_name=offer_name,
        price=offer_price,
        service_type=service_type,
    )


def respond_node(state: AgentState) -> AgentState:
    """Stage 4: RESPOND Node.

    Drives the reply from the conversation stage (Manar's multi-turn design):
    EXPLAIN_OFFER / HANDLE_OBJECTION / CLOSE_DEAL / ROUTE_TO_PAYMENT, falling
    back to the initial engagement flow (Groq pitch or template). The offer
    payload and action contract stay compatible with the integration API.
    """
    customer = state.get("customer_data") or {}
    recommendation = state.get("recommendation") or {}
    stage = state.get("conversation_stage")
    trigger = state.get("trigger_reason")

    primary_offer = recommendation.get("primary")

    if trigger == "customer_not_found" or not customer:
        state["response"] = "Customer profile could not be found. How can I assist you today?"
        state["offer"] = None
        state["action"] = "ask_question"
        return state

    customer_name = customer.get("name") or "valued customer"

    if not primary_offer:
        state["response"] = _general_no_offer_response(customer_name)
        state["offer"] = None
        state["action"] = "ask_question"
        return state

    offer_name = _offer_name(primary_offer)
    offer_price = primary_offer.get("price")
    features = primary_offer.get("features") or []
    state["offer"] = {
        "product": offer_name,
        "price": offer_price,
        "description": primary_offer.get("description", ""),
    }

    if stage == "EXPLAIN_OFFER":
        state["response"] = explain_offer_template(
            product_name=offer_name,
            features=features,
        )
        state["action"] = "offer_explained"
        return state

    if stage == "HANDLE_OBJECTION":
        customer_context = {
            "customer_name": customer_name,
            "current_plan": customer.get("current_plan"),
            "service_type": customer.get("service_type"),
            "speed": customer.get("speed"),
            "usage_percentage": customer.get("usage_percentage"),
            "usage_meaning": (
                "Percentage of speed utilized"
                if customer.get("service_type") == "fiber_home"
                else "Percentage of mobile data allowance used"
                if customer.get("service_type") == "mobile_data"
                else "Unspecified usage measure"
            ),
            "segment": customer.get("segment"),
        }

        try:
            state["response"] = generate_stage_response(
                stage=stage,
                customer_context=customer_context,
                product_info=primary_offer,
                customer_message=state.get("message", ""),
            )
        except Exception as exc:  # noqa: BLE001 - LLM may be unavailable
            print(f"[Responses] Groq objection handling failed, using template: {exc}")
            state["response"] = explain_offer_template(
                product_name=offer_name,
                features=features[:2],
            )
        state["action"] = "objection_handled"
        return state

    if stage == "CLOSE_DEAL":
        state["response"] = close_and_route_template(
            product_name=offer_name,
            features=features,
            product_page_url=MOCK_PRODUCT_PAGE_URL,
        )
        state["action"] = "deal_closed"
        return state

    if stage == "ROUTE_TO_PAYMENT":
        state["response"] = (
            f"You can continue to the payment step for "
            f"the {offer_name}."
        )
        state["action"] = "route_to_payment"
        return state

    # ENGAGE or no recognized stage: present the initial offer.
    state["response"] = _engagement_response(
        message=state.get("message") or "",
        trigger=trigger,
        customer_name=customer_name,
        usage=int(customer.get("usage_percentage") or 0),
        current_plan=customer.get("current_plan") or "",
        service_type=customer.get("service_type"),
        offer_name=offer_name,
        offer_price=offer_price,
    )
    state["action"] = "show_offer"
    return state