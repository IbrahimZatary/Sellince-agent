import os

from app.agent.agent_state import AgentState
from app.agent.offer_history import was_offer_recently_sent
from app.agent.respond import _get_client
from app.core.database import SessionLocal
from app.models.customer import Customer


def _no_offer() -> dict:
    """Nothing to announce.

    Also clears any offer left in the state, so an offer that was never
    shown to the customer cannot leak into the next chat turn.
    """
    return {
        "active_offer": None,
        "recommendation": None,
        "offer": None,
        "response": None,
    }


def _pct(value) -> str:
    try:
        return f"{float(value):g}"
    except (TypeError, ValueError):
        return str(value)


def _reason(customer: dict, trigger: str | None) -> str:
    """One customer-facing sentence: why we are reaching out."""
    usage = _pct(customer.get("usage_percentage"))

    if trigger == "mobile_data_upgrade":
        return f"You've used {usage}% of your mobile data."

    if trigger == "fiber_speed_upgrade":
        return (
            f"Your home internet is running at {usage}% "
            "of its speed capacity."
        )

    if trigger == "retention_offer":
        end_date = customer.get("contract_end_date")

        if end_date:
            return f"Your contract ends on {end_date}."

        return "Your contract is ending soon."

    if trigger == "5g_offer":
        return "You've shown interest in 5G."

    if trigger == "fiber_cross_sell":
        return (
            "A home fiber connection could work well "
            "alongside your mobile plan."
        )

    return ""


def _opening_message(
    customer: dict,
    offer: dict,
    trigger: str | None,
) -> str:
    name = customer.get("name") or "there"
    product_name = offer.get("product_name") or offer.get("name")
    price = offer.get("price")
    reason = _reason(customer, trigger)

    offer_line = f"We have {product_name} available"
    offer_line += f" for {price} JOD." if price is not None else "."

    fallback = " ".join(
        part
        for part in (
            f"Hi {name}!",
            reason,
            offer_line,
            "Would you like to know more?",
        )
        if part
    )

    client = _get_client()

    if client is None:
        return fallback

    prompt = (
        "You are a friendly telecom sales assistant. "
        "Write a short personalized opening message "
        "(2-3 sentences maximum). "
        f"Customer name: {name}. "
        f"Current plan: {customer.get('current_plan')}. "
        f"Reason for reaching out: {reason or 'none'}. "
        f"Offer: {product_name}. "
        f"Price: {price} JOD. "
        "Mention the reason naturally, introduce the offer, "
        "and end with a soft question. "
        "Do not invent any offer details."
    )

    try:
        completion = client.chat.completions.create(
            model=os.getenv("GROQ_MODEL", "openai/gpt-oss-20b"),
            messages=[{"role": "system", "content": prompt}],
            temperature=0.3,
            max_tokens=500,
            reasoning_effort="low",
        )

        text = (completion.choices[0].message.content or "").strip()

    except Exception as exc:
        print(f"[Proactive] Groq failed, using fallback: {exc}")
        return fallback

    return text or fallback


def proactive_offer_node(state: AgentState) -> dict:
    """Compose the opening message for a proactive session.

    This node no longer decides anything. detect_node found the trigger
    and recommend_node chose the offer, exactly as in a normal chat.
    Here we only apply the repeat-offer cooldown and write the message.
    """
    customer = state.get("customer_data")
    offer = state.get("offer") or state.get("recommendation")

    if not customer or not isinstance(offer, dict):
        return _no_offer()

    product_name = offer.get("product_name") or offer.get("name")

    if not product_name:
        return _no_offer()

    customer_id = state["customer_id"]

    db = SessionLocal()

    try:
        company_id = (
            db.query(Customer.company_id)
            .filter(Customer.id == customer_id)
            .scalar()
        )

        already_sent = was_offer_recently_sent(
            db=db,
            customer_id=customer_id,
            company_id=company_id,
            product_name=product_name,
        )

    finally:
        db.close()

    if already_sent:
        return _no_offer()

    opening_message = _opening_message(
        customer=customer,
        offer=offer,
        trigger=state.get("trigger_reason"),
    )

    return {
        "active_offer": offer,
        "recommendation": offer,
        "offer": offer,
        "response": opening_message,
        "conversation_stage": "ENGAGE",
    }