import json
import re
from datetime import date
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


def load_products() -> list[dict]:
    with PRODUCTS_FILE.open(
        "r",
        encoding="utf-8",
    ) as file:
        return json.load(file)


def extract_amount(
    value: str | None,
    unit: str,
) -> Decimal | None:
    match = re.search(
        rf"(\d+(?:\.\d+)?)\s*{re.escape(unit)}\b",
        value or "",
        flags=re.IGNORECASE,
    )

    return (
        Decimal(match.group(1))
        if match
        else None
    )


def get_upgrade_candidates(
    customer: Customer,
) -> tuple[str | None, list[int]]:
    rule = UPGRADE_RULES.get(
        customer.service_type
    )

    if rule is None:
        return None, []

    product_type = rule["product_type"]

    if (
        customer.usage_percentage
        < rule["threshold"]
    ):
        return product_type, []

    current_value = (
        customer.current_plan
        if customer.service_type == "mobile_data"
        else customer.speed
    )

    current_amount = extract_amount(
        current_value,
        rule["unit"],
    )

    if current_amount is None:
        return product_type, []

    products = load_products()
    larger_products = []

    for product in products:
        if product["type"] != product_type:
            continue

        product_value = (
            product["name"]
            if customer.service_type
            == "mobile_data"
            else product["speed"]
        )

        amount = extract_amount(
            product_value,
            rule["unit"],
        )

        if (
            amount is not None
            and amount > current_amount
        ):
            larger_products.append(
                (
                    amount,
                    product["product_id"],
                )
            )

    if not larger_products:
        return product_type, []

    next_amount = min(
        amount
        for amount, _ in larger_products
    )

    eligible_ids = [
        product_id
        for amount, product_id
        in larger_products
        if amount == next_amount
    ]

    return product_type, eligible_ids


def is_already_on_5g(
    customer: Customer,
) -> bool:
    current_plan = (
        customer.current_plan or ""
    )
    current_speed = (
        customer.speed or ""
    )

    return (
        "5G" in current_plan.upper()
        or current_speed.upper() == "5G"
    )


def is_interested_in_5g(
    customer: Customer,
) -> bool:
    interests = customer.interests or ""

    return "5G" in interests.upper()


def get_5g_candidates(
    customer: Customer,
) -> list[int]:
    if (
        customer.service_type
        != "mobile_data"
    ):
        return []

    if not is_interested_in_5g(customer):
        return []

    if is_already_on_5g(customer):
        return []

    products = load_products()

    # The use case specifies "Switch to 5G plan".
    # Therefore, candidates must be Mobile Data
    # plans whose speed is 5G, not Add-on products.
    return [
        product["product_id"]
        for product in products
        if (
            product["type"] == "Mobile Data"
            and str(
                product.get("speed", "")
            ).upper() == "5G"
        )
    ]


def has_fiber_cross_sell_eligibility(
    customer: Customer,
) -> bool:
    """
    The PDF requires:
        service_type = mobile_data
        + location = fiber area

    The mock data does not define a complete fiber
    coverage map, so this function does not invent one.

    A mobile customer must have a location value before
    the cross-sell can be considered further.
    """

    if (
        customer.service_type
        != "mobile_data"
    ):
        return False

    location = getattr(
        customer,
        "location",
        None,
    )

    return bool(location)


def get_fiber_cross_sell_candidates(
    customer: Customer,
) -> list[int]:
    if not has_fiber_cross_sell_eligibility(
        customer
    ):
        return []

    products = load_products()

    # The PDF specifies "Offer Fiber Home Internet",
    # so only Fiber Home products are candidates.
    return [
        product["product_id"]
        for product in products
        if product["type"] == "Fiber Home"
    ]


def build_customer_search_query(
    customer: Customer,
) -> str:
    return (
        f"Offer for a "
        f"{customer.service_type} customer. "
        f"Current plan: "
        f"{customer.current_plan}. "
        f"Current speed: "
        f"{customer.speed or 'Unknown'}. "
        f"Usage: "
        f"{customer.usage_percentage}%. "
        f"Segment: "
        f"{customer.segment or 'General'}. "
        f"Interests: "
        f"{customer.interests or 'Not specified'}."
    )


def get_upgrade_recommendation(
    customer: Customer,
) -> dict:
    product_type, eligible_ids = (
        get_upgrade_candidates(customer)
    )

    if not eligible_ids:
        return {}

    recommendation = search_products(
        query=build_customer_search_query(
            customer
        ),
        product_type=product_type,
        eligible_product_ids=eligible_ids,
    )

    if not recommendation:
        return {}

    recommendation["offer_type"] = (
        "upgrade"
    )

    return recommendation


def get_5g_recommendation(
    customer: Customer,
) -> dict:
    eligible_ids = get_5g_candidates(
        customer
    )

    if not eligible_ids:
        return {}

    recommendation = search_products(
        query=(
            "5G Mobile Data plan for a mobile "
            "customer interested in switching "
            "to a 5G plan."
        ),
        product_type="Mobile Data",
        eligible_product_ids=eligible_ids,
    )

    if not recommendation:
        return {}

    recommendation["offer_type"] = (
        "5g_offer"
    )

    return recommendation


def get_fiber_cross_sell_recommendation(
    customer: Customer,
) -> dict:
    eligible_ids = (
        get_fiber_cross_sell_candidates(
            customer
        )
    )

    if not eligible_ids:
        return {}

    recommendation = search_products(
        query=(
            "Fiber Home Internet offer for "
            "a mobile data customer located "
            "in a fiber-eligible area."
        ),
        product_type="Fiber Home",
        eligible_product_ids=eligible_ids,
    )

    if not recommendation:
        return {}

    recommendation["offer_type"] = (
        "fiber_cross_sell"
    )

    return recommendation


def get_retention_recommendation(
    customer: Customer,
) -> dict:
    end_date = getattr(
        customer,
        "contract_end_date",
        None,
    )

    if not end_date:
        return {}

    if isinstance(end_date, str):
        end_date = date.fromisoformat(
            end_date
        )

    days_remaining = (
        end_date - date.today()
    ).days

    if not 0 <= days_remaining <= 30:
        return {}

    return {
        "offer_type": "retention",
        "reason": "contract_expiring",
        "contract_end_date": (
            end_date.isoformat()
        ),
        "days_remaining": days_remaining,
        "message": (
            "The customer's contract is "
            "approaching its end date. "
            "A renewal or retention offer "
            "may be appropriate."
        ),
    }


def get_recommendations_for_triggers(
    customer: Customer,
    trigger_reasons: list[str] | None,
) -> list[dict]:
    """
    Build recommendations only from opportunities
    detected by the trigger layer.
    """

    triggers = set(
        trigger_reasons or []
    )

    recommendations = []

    if (
        "high_data_usage" in triggers
        or "high_fiber_usage" in triggers
    ):
        upgrade = (
            get_upgrade_recommendation(
                customer
            )
        )

        if upgrade:
            recommendations.append(
                upgrade
            )

    if "5g_interest" in triggers:
        five_g = get_5g_recommendation(
            customer
        )

        if five_g:
            recommendations.append(
                five_g
            )

    if "fiber_cross_sell" in triggers:
        fiber_cross_sell = (
            get_fiber_cross_sell_recommendation(
                customer
            )
        )

        if fiber_cross_sell:
            recommendations.append(
                fiber_cross_sell
            )

    if "contract_expiring" in triggers:
        retention = (
            get_retention_recommendation(
                customer
            )
        )

        if retention:
            recommendations.append(
                retention
            )

    return recommendations


def get_customer_product_recommendations(
    customer: Customer,
) -> list[dict]:
    """
    General recommendation path for standalone
    tools that do not provide trigger information.
    """

    recommendations = []

    upgrade = get_upgrade_recommendation(
        customer
    )

    if upgrade:
        recommendations.append(upgrade)

    five_g = get_5g_recommendation(
        customer
    )

    if five_g:
        recommendations.append(five_g)

    fiber_cross_sell = (
        get_fiber_cross_sell_recommendation(
            customer
        )
    )

    if fiber_cross_sell:
        recommendations.append(
            fiber_cross_sell
        )

    retention = (
        get_retention_recommendation(
            customer
        )
    )

    if retention:
        recommendations.append(
            retention
        )

    return recommendations


def recommend_products_for_customer(
    customer: Customer,
    trigger_reasons: list[str] | None = None,
) -> list[dict]:
    """
    Return all valid recommendations.

    Agent calls provide trigger_reasons.
    Standalone tools may use the general path.
    """

    if trigger_reasons is not None:
        return (
            get_recommendations_for_triggers(
                customer=customer,
                trigger_reasons=trigger_reasons,
            )
        )

    return (
        get_customer_product_recommendations(
            customer
        )
    )


def recommend_product_for_customer(
    customer: Customer,
    trigger_reasons: list[str] | None = None,
) -> dict:
    """
    Backward-compatible single recommendation
    entry point.
    """

    recommendations = (
        recommend_products_for_customer(
            customer=customer,
            trigger_reasons=trigger_reasons,
        )
    )

    if not recommendations:
        return {}

    return recommendations[0]