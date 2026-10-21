
import json
import urllib.error
import urllib.request

from app.core.database import SessionLocal
from app.models.customer import Customer


BASE_URL = "http://127.0.0.1:8000/api/v1"


def send_request(endpoint: str, data: dict) -> dict:
    request = urllib.request.Request(
        url=f"{BASE_URL}{endpoint}",
        data=json.dumps(data).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            return json.loads(response.read().decode("utf-8"))

    except urllib.error.HTTPError as error:
        details = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(
            f"HTTP {error.code}: {details}"
        ) from error

    except urllib.error.URLError as error:
        raise RuntimeError(
            f"Could not connect to backend: {error.reason}"
        ) from error


def get_customer(customer_id: int):
    with SessionLocal() as db:
        return (
            db.query(Customer)
            .filter(Customer.id == customer_id)
            .first()
        )


def print_offer(offer: dict | None) -> None:
    if not offer:
        return

    print("\n--- OFFER ---")
    print("Product:", offer.get("product_name"))
    print("Price:", offer.get("price"), "JOD")


def print_debug(data: dict) -> None:
    print("\n--- DEBUG ---")

    if data.get("conversation_stage"):
        print("Stage:", data["conversation_stage"])

    if data.get("action"):
        print("Action:", data["action"])

    print_offer(data.get("offer"))

    print("-" * 60)


def main() -> None:
    print("=" * 60)
    print("SELLINCE - PROACTIVE + INTERACTIVE AI AGENT")
    print("=" * 60)

    while True:
        customer_input = input(
            "\nEnter Customer ID (or exit): "
        ).strip()

        if customer_input.lower() in {"exit", "quit"}:
            return

        if not customer_input.isdigit():
            print("Invalid customer ID.")
            continue

        customer_id = int(customer_input)
        customer = get_customer(customer_id)

        if customer is None:
            print("Customer not found.")
            continue

        print("\n--- CUSTOMER PROFILE ---")
        print("ID:", customer.id)
        print("Name:", customer.name)
        print("Plan:", customer.current_plan)
        print("Usage:", customer.usage_percentage, "%")
        print("Segment:", customer.segment)
        print("Service:", customer.service_type)

        print("\nStarting Proactive Session...")

        try:
            session = send_request(
                "/agent/start-session",
                {"customer_id": customer_id},
            )
        except RuntimeError as error:
            print("Error:", error)
            continue

        conversation_id = session.get("conversation_id")

        print("\nConversation ID:", conversation_id)
        print("Session Status:", session.get("status"))

        if session.get("response"):
            print("\nPROACTIVE AGENT:")
            print(session["response"])
            print_offer(session.get("offer"))
        elif session.get("status") == "existing":
            print(
                "\nExisting session: proactive will not repeat."
            )
        else:
            print("\nNo proactive offer was generated.")

        print("\n" + "-" * 60)
        print("Chat started!")
        print("Type 'back' to select another customer.")
        print("Type 'exit' to quit.")
        print("-" * 60)

        while True:
            message = input("\nYOU: ").strip()

            if message.lower() in {"exit", "quit"}:
                return

            if message.lower() == "back":
                break

            if not message:
                continue

            try:
                reply = send_request(
                    "/chat",
                    {
                        "customer_id": customer_id,
                        "message": message,
                    },
                )
            except RuntimeError as error:
                print("Error:", error)
                continue

            print("\nAGENT:")
            print(reply.get("response") or "(No response)")

            print_debug(reply)


if __name__ == "__main__":
    main()
