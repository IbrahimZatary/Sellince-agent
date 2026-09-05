def initial_engagement_template(
    customer_name: str,
    usage_percentage: float,
    current_plan: str,
    product_name: str,
    price: float,
) -> str:
    return (
        f"Hi {customer_name},\n"
        f"I noticed you're using {usage_percentage}% of your {current_plan}.\n"
        f"We have a great offer: {product_name} for just {price} JOD.\n"
        f"Would you like to hear more about it?"
    )


def explain_offer_template(
    product_name: str,
    feature_1: str,
    feature_2: str,
    feature_3: str,
    target_segment: str,
) -> str:
    return (
        f"Great! Here are the details:\n"
        f"{product_name} includes:\n"
        f"- {feature_1}\n"
        f"- {feature_2}\n"
        f"- {feature_3}\n"
        f"This is designed for {target_segment}.\n"
        f"Would you like to proceed with this offer?"
    )


def close_and_route_template(
    product_name: str,
    feature_1: str,
    feature_2: str,
    feature_3: str,
    product_page_url: str,
) -> str:
    return (
        f"Excellent! You've selected the {product_name}.\n"
        f"Click here to continue with your upgrade: {product_page_url}\n"
        f"Your selected plan includes:\n"
        f"- {feature_1}\n"
        f"- {feature_2}\n"
        f"- {feature_3}\n"
        f"Thank you for choosing us!"
    )