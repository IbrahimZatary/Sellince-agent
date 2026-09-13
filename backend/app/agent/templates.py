def initial_engagement_template(
    customer_name: str,
    usage_percentage: float,
    current_plan: str,
    product_name: str,
    price: float,
    *,
    service_type: str | None = None,
) -> str:
    if service_type == "fiber_home":
        usage_message = (
            f"Your recorded speed utilization is "
            f"{usage_percentage}% on your {current_plan}."
        )
    elif service_type == "mobile_data":
        usage_message = (
            f"You've used {usage_percentage}% of the data "
            f"in your {current_plan}."
        )
    else:
        usage_message = (
            f"Your recorded usage is {usage_percentage}% "
            f"on your {current_plan}."
        )

    return (
        f"Hi {customer_name},\n"
        f"{usage_message}\n"
        f"An upgrade option is {product_name}, "
        f"listed at {price} JOD.\n"
        "Would you like to hear more about it?"
    )


def _format_features(features: list[str]) -> str:
    available = [
        feature.strip()
        for feature in features
        if feature
        and feature.strip()
        and feature.strip() != "Feature information unavailable"
    ]

    return "\n".join(f"- {feature}" for feature in available)


def explain_offer_template(
    product_name: str,
    feature_1: str = "",
    feature_2: str = "",
    feature_3: str = "",
    target_segment: str = "",
    *,
    features: list[str] | None = None,
) -> str:
    selected_features = (
        features
        if features is not None
        else [feature_1, feature_2, feature_3]
    )

    feature_text = _format_features(selected_features)
    details = f"\n{feature_text}" if feature_text else ""

    return (
        f"Here are the details of {product_name}:"
        f"{details}\n"
        "Would you like to proceed with this offer?"
    )


def close_and_route_template(
    product_name: str,
    feature_1: str = "",
    feature_2: str = "",
    feature_3: str = "",
    product_page_url: str = "",
    *,
    features: list[str] | None = None,
) -> str:
    selected_features = (
        features
        if features is not None
        else [feature_1, feature_2, feature_3]
    )

    feature_text = _format_features(selected_features)

    details = (
        f"\nYour selected product includes:\n{feature_text}"
        if feature_text
        else ""
    )

    next_step = (
        f"\nReview the next step here: {product_page_url}"
        if product_page_url
        else ""
    )

    return (
        f"You've selected {product_name}."
        f"{details}"
        f"{next_step}\n"
        "Your subscription has not been changed."
    )