
import os

from app.agent.agent_state import AgentState
from app.agent.proactive_scoring import select_best_offer_type
from app.agent.proactive_offer_resolver import resolve_proactive_offer
from app.agent.customer_profile import build_customer_profile
from app.agent.respond import _get_client
from app.core.database import SessionLocal
from app.models.customer import Customer
from app.agent.offer_history import was_offer_recently_sent

def proactive_offer_node(state: AgentState) -> dict:
    db = SessionLocal()

    try:
        customer = db.query(Customer).filter(
            Customer.id == state["customer_id"]
        ).first()

        if customer is None:
            return {
                "response": "Customer not found.",
                "active_offer": None,
            }

        profile = build_customer_profile(customer)

        offer_type = select_best_offer_type(profile)

        product = resolve_proactive_offer(
            customer=customer,
            offer_type=offer_type,
        )

        if not product:
            return {
                "customer_profile": profile,
                "active_offer": None,
                "response": None,
            }
        already_sent = was_offer_recently_sent(
    db=db,
    customer_id=customer.id,
    company_id=customer.company_id,
    product_name=product["product_name"],
)

        if already_sent:
            return {
                "customer_profile": profile,
                "active_offer": None,
                "response": None,
            }

        client = _get_client()

        if client:
            prompt = (
                "You are a friendly telecom sales assistant. "
                "Write a short personalized opening message "
                "(2-3 sentences maximum). "
                f"Customer name: {profile['name']}. "
                f"Current plan: {profile['current_plan']}. "
                f"Usage: {profile['usage_percentage']}%. "
                f"Offer: {product['product_name']}. "
                f"Price: {product['price']} JOD. "
                "Mention the customer's usage naturally, "
                "introduce the offer, and end with a soft question. "
                "Do not invent any offer details."
            )

            
            completion = client.chat.completions.create(
                model=os.getenv("GROQ_MODEL", "openai/gpt-oss-20b"),
                messages=[
                    {"role": "system", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=500,
                reasoning_effort="low",
            )

            opening_message = completion.choices[0].message.content.strip()

        else:
            opening_message = (
                f"Hi {profile['name']}! "
                f"You've used {profile['usage_percentage']}% "
                f"of your current plan. "
                f"We have {product['product_name']} available. "
                "Would you like to know more?"
            )

        return {
            "customer_profile": profile,
            "active_offer": product,
            "recommendation": {"primary": product},
            "response": opening_message,
            "conversation_stage": "ENGAGE",
        }

    finally:
        db.close()
