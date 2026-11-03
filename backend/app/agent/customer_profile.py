
from app.models.customer import Customer


def build_customer_profile(customer: Customer) -> dict:
    return {
        "customer_id": customer.id,
        "name": customer.name,
        "current_plan": customer.current_plan,
        "usage_percentage": float(customer.usage_percentage),
        "segment": customer.segment,
        "service_type": customer.service_type,
        "months_active": None,
        "has_active_addon": None,
        "has_vip_offer": None,
        "last_payment_status": None,
        "preferred_language": None,
    }
