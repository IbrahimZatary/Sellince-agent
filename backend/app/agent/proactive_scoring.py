
def select_best_offer_type(profile: dict) -> str:
    signals = []

    # 1. Data Usage
    usage = profile.get("usage_percentage")

    if usage is not None and usage >= 85:
        signals.append(("upgrade_data_plan", 0.90))

    # 2. Loyalty
    months_active = profile.get("months_active")
    has_active_addon = profile.get("has_active_addon")

    if (
        months_active is not None
        and months_active >= 6
        and has_active_addon is False
    ):
        signals.append(("loyalty_addon", 0.75))

    # 3. VIP Customer
    segment = profile.get("segment")
    has_vip_offer = profile.get("has_vip_offer")

    if segment == "high_value" and has_vip_offer is False:
        signals.append(("vip_bundle", 0.88))

    # 4. Payment Status
    payment_status = profile.get("last_payment_status")

    if payment_status == "failed":
        signals.append(("flexible_payment_plan", 0.80))

    # 5. Default
    if not signals:
        return "default_discovery"

    # Select the highest score
    best_offer = max(signals, key=lambda x: x[1])

    return best_offer[0]
