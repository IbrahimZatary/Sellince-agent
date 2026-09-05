from app.agent.templates import (
    initial_engagement_template,
    explain_offer_template,
    close_and_route_template,
)


def main() -> None:
    print("\n--- TEMPLATE 1 ---")
    print(
        initial_engagement_template(
            customer_name="Ahmed Al-Fayez",
            usage_percentage=92,
            current_plan="20GB Data Plan",
            product_name="50GB Data Plan",
            price=25,
        )
    )

    print("\n--- TEMPLATE 2 ---")
    print(
        explain_offer_template(
            product_name="50GB Data Plan",
            feature_1="5G speed",
            feature_2="Unlimited calls",
            feature_3="Free streaming",
            target_segment="Heavy User",
        )
    )

    print("\n--- TEMPLATE 3 ---")
    print(
        close_and_route_template(
            product_name="50GB Data Plan",
            feature_1="5G speed",
            feature_2="Unlimited calls",
            feature_3="Free streaming",
            product_page_url="/mock/product",
        )
    )


if __name__ == "__main__":
    main()