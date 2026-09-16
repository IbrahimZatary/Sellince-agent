from app.core.database import SessionLocal
from app.services.customer_service import search_customer_by_name
from app.rag.customer_recommendation import recommend_product_for_customer
from app.rag.response_generator import generate_response

def main():
    db = SessionLocal()

    try:
        customer_name = "YOUSEF AL-OMARI"

        print(f"Searching for customer: {customer_name}")

        customers = search_customer_by_name(db, customer_name)

        if not customers:
            print("Customer not found.")
            return

        customer = customers[0]

        print("\n--- CUSTOMER FOUND ---")


        print(f"Name: {customer.name}")
        print(f"Current Plan: {customer.current_plan}")
        print(f"Usage: {customer.usage_percentage}%")
        print(f"Segment: {customer.segment}")

        print("\n--- RAG PRODUCT RETRIEVAL ---")

     
        product = recommend_product_for_customer(customer)

        print(f"Product: {product['product_name']}")
        print(f"Price: {product['price']} JOD")
        print(f"Description: {product['description']}")
        print(f"Target Segment: {product['target_segment']}")

        print("\n--- LLM GENERATED RESPONSE ---")

        customer_context = {
            "customer_name": customer.name,
            "current_plan": customer.current_plan,
            "usage_percentage": str(customer.usage_percentage),
            "segment": customer.segment,
        }

        response = generate_response(
            customer_context=customer_context,
            product_info=product,
        )

        print(response)
     
    finally:
        db.close()


if __name__ == "__main__":
    main()