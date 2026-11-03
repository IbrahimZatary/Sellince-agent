
from app.models.customer import Customer
from app.rag.customer_recommendation import recommend_product_for_customer


def resolve_proactive_offer(
    customer: Customer,
    offer_type: str,
) -> dict:

    if offer_type == "upgrade_data_plan":
        return recommend_product_for_customer(customer)

    return {}
