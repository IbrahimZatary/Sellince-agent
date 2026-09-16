from app.agent.runner import run_agent_turn


CONVERSATION_ID = 1
CUSTOMER_ID = 1


def run_turn(message: str) -> None:
    state = {
        "customer_id": CUSTOMER_ID,
        "message": message,
    }

    result = run_agent_turn(
        conversation_id=CONVERSATION_ID,
        state=state,
    )

    print("\n" + "=" * 60)
    print("CUSTOMER:", message)
    print("INTENT:", result.get("intent"))
    print("STAGE:", result.get("conversation_stage"))
    print("PRODUCT:", result.get("recommendation"))
    print("ACTION:", result.get("action"))

    print("\nAGENT:")
    print(result.get("response"))


def main() -> None:
    run_turn("Can you tell me more about this offer?")
    run_turn("25 JOD is too expensive.")
    run_turn("Okay, I want the offer.")
    run_turn("Yes, I am ready to proceed with payment.")


if __name__ == "__main__":
    main()