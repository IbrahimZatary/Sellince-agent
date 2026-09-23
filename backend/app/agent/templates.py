def initial_engagement_template(
    customer_name: str,
    usage_percentage: float,
    current_plan: str,
    product_name: str,
    price: float,
    *,
    service_type: str | None = None,
) -> str:
    return (
        f"Hi {customer_name},\n"
        f"I noticed you're using {usage_percentage}% of your {current_plan}.\n"
        f"We have a great offer: {product_name} for just {price} JOD.\n"
        "Would you like to hear more about it?"
    )


def _get_three_features(
    features: list[str],
) -> list[str]:
    available = [
        feature.strip()
        for feature in features
        if feature
        and feature.strip()
        and feature.strip() != "Feature information unavailable"
    ]

    return available[:3]


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

    selected_features = _get_three_features(selected_features)

    feature_lines = "\n".join(
        f"• {feature}"
        for feature in selected_features
    )

    return (
        "Great! Here are the details:\n"
        f"{product_name} includes:\n"
        f"{feature_lines}\n"
        f"This is perfect for {target_segment} like you.\n"
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

    selected_features = _get_three_features(selected_features)

    feature_lines = "\n".join(
        f"• {feature}"
        for feature in selected_features
    )

    product_link = (
        product_page_url
        if product_page_url
        else "[Link to Mock Product Page]"
    )

    return (
        f"Excellent! Your new {product_name} will be activated now.\n"
        f"Click here to complete your upgrade: {product_link}\n"
        "Your new plan includes:\n"
        f"{feature_lines}\n"
        "Thank you for choosing us!"
    )