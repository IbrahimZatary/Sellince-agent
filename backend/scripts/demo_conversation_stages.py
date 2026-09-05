from understand import understand_node
from respond import respond_node


BASE_STATE = {
    "customer_data": {
        "name": "Ahmed",
        "current_plan": "20GB Data Plan",
        "usage_percentage": "92",
        "segment": "Heavy User",
    },
    "recommendation": {
        "primary": {
            "product_name": "50GB Data Plan",
            "price": 25,
            "description": (
                "50GB data with 5G speed, "
                "unlimited calls, and free streaming."
            ),
            "target_segment": "Heavy User",
        }
    },
    "trigger_reason": None,
}


TEST_MESSAGES = [
    "Can you tell me more about this offer?",
    "25 JOD is too expensive.",
    "Okay, I want the offer.",
    "Yes, I am ready to proceed with payment.",
]


def run_test(message: str) -> None:
    state = BASE_STATE.copy()
    state["message"] = message

    state = understand_node(state)
    state = respond_node(state)

    print("\n" + "=" * 60)
    print(f"CUSTOMER: {message}")
    print(f"INTENT: {state['intent']}")
    print(f"STAGE: {state['conversation_stage']}")
    print(f"ACTION: {state['action']}")
    print("\nAGENT RESPONSE:")
    print(state["response"])


def main():
    for message in TEST_MESSAGES:
        run_test(message)


if __name__ == "__main__":
    main()