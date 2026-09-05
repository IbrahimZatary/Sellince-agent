from app.agent.runner import run_agent_turn
from app.core.database import SessionLocal
from app.models.customer import Customer
from app.models.conversation import Conversation


def get_customer(db, customer_id: int) -> Customer | None:
    return (
        db.query(Customer)
        .filter(Customer.id == customer_id)
        .first()
    )


def get_or_create_open_conversation(
    db,
    customer: Customer,
) -> Conversation:
    conversation = (
        db.query(Conversation)
        .filter(
            Conversation.customer_id == customer.id,
            Conversation.company_id == customer.company_id,
            Conversation.status == "open",
        )
        .order_by(Conversation.started_at.desc())
        .first()
    )

    if conversation:
        return conversation

    conversation = Conversation(
        customer_id=customer.id,
        company_id=customer.company_id,
        status="open",
    )

    db.add(conversation)
    db.commit()
    db.refresh(conversation)

    return conversation


def main() -> None:
    db = SessionLocal()

    try:
        print("=" * 60)
        print("Sellince Interactive Agent")
        print("=" * 60)

        customer_id_input = input(
            "\nEnter customer ID: "
        ).strip()

        if not customer_id_input.isdigit():
            print("Invalid customer ID.")
            return

        customer_id = int(customer_id_input)

        customer = get_customer(
            db=db,
            customer_id=customer_id,
        )

        if customer is None:
            print(
                f"Customer with ID {customer_id} was not found."
            )
            return

        conversation = get_or_create_open_conversation(
            db=db,
            customer=customer,
        )

        print("\nCustomer found:")
        print(f"Name: {customer.name}")
        print(f"Plan: {customer.current_plan}")
        print(f"Usage: {customer.usage_percentage}%")
        print(f"Segment: {customer.segment}")

        print(
            f"\nConversation ID: {conversation.id}"
        )

        print("\nType 'exit' to stop.")
        print("-" * 60)

        while True:
            message = input("\nYou: ").strip()

            if message.lower() in {
                "exit",
                "quit",
            }:
                print("\nConversation ended.")
                break

            if not message:
                continue

            state = {
                "customer_id": customer.id,
                "message": message,
            }

            result = run_agent_turn(
                conversation_id=conversation.id,
                state=state,
            )

            print("\nAgent:")
            print(result.get("response"))

            print("\n--- Debug ---")
            print(
                "Intent:",
                result.get("intent"),
            )
            print(
                "Stage:",
                result.get("conversation_stage"),
            )
            print(
                "Action:",
                result.get("action"),
            )
            print(
                "Product:",
                result.get("recommendation"),
            )

    finally:
        db.close()


if __name__ == "__main__":
    main()