import json
import re
from decimal import Decimal

from app.models.customer import Customer
from app.rag.config import PRODUCTS_FILE
from app.rag.retriever import search_products


UPGRADE_RULES = {
    "mobile_data": {
        "product_type": "Mobile Data",
        "threshold": 90,
        "unit": "GB",
    },
    "fiber_home": {
        "product_type": "Fiber Home",
        "threshold": 85,
        "unit": "Mbps",
    },
}


def extract_amount(value: str | None, unit: str) -> Decimal | None:
    match = re.search(
        rf"(\d+(?:\.\d+)?)\s*{re.escape(unit)}\b",
        value or "",
        flags=re.IGNORECASE,
    )

    return Decimal(match.group(1)) if match else None


def get_upgrade_candidates(customer: Customer) -> tuple[str | None, list[int]]:
    rule = UPGRADE_RULES.get(customer.service_type)

    if rule is None:
        return None, []

    product_type = rule["product_type"]

    if customer.usage_percentage < rule["threshold"]:
        return product_type, []

    current_value = (
        customer.current_plan
        if customer.service_type == "mobile_data"
        else customer.speed
    )
    current_amount = extract_amount(current_value, rule["unit"])

    if current_amount is None:
        return product_type, []

    with PRODUCTS_FILE.open("r", encoding="utf-8") as file:
        products = json.load(file)

    larger_products = []

    for product in products:
        if product["type"] != product_type:
            continue

        product_value = (
            product["name"]
            if customer.service_type == "mobile_data"
            else product["speed"]
        )
        amount = extract_amount(product_value, rule["unit"])

        if amount is not None and amount > current_amount:
            larger_products.append((amount, product["product_id"]))

    if not larger_products:
        return product_type, []

    next_amount = min(amount for amount, _ in larger_products)

    eligible_ids = [
        product_id
        for amount, product_id in larger_products
        if amount == next_amount
    ]

    return product_type, eligible_ids


def build_customer_search_query(customer: Customer) -> str:
    return (
        f"Upgrade for a {customer.service_type} customer. "
        f"Current plan: {customer.current_plan}. "
        f"Current speed: {customer.speed or 'Unknown'}. "
        f"Segment: {customer.segment or 'General'}. "
        f"Interests: {customer.interests or 'Not specified'}."
    )


def recommend_product_for_customer(customer: Customer) -> dict:
    product_type, eligible_ids = get_upgrade_candidates(customer)

    if not eligible_ids:
        return {}

    return search_products(
        query=build_customer_search_query(customer),
        product_type=product_type,
        eligible_product_ids=eligible_ids,
    )