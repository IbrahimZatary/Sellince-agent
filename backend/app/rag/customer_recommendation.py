from app.models.customer import Customer
from app.rag.retriever import search_products

def build_customer_search_query(customer: Customer) -> str:
    segment = customer.segment or "General"

    return (
        f"{segment} customer with "
        f"{customer.usage_percentage}% usage"
    )


def recommend_product_for_customer(customer: Customer) -> dict:
    query = build_customer_search_query(customer)

    return search_products(query)
