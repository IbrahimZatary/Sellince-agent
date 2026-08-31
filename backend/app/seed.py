"""Demo data seed for the Sellince backend.

Run from the ``backend/`` directory:

    python3 -m app.seed                              # idempotent: insert only missing rows
    python3 -m app.seed --reset                      # TRUNCATE all tables, then seed fresh (ids restart at 1)
    python3 -m app.seed --scale small|medium|large   # data volume (default: medium)
"""

import sys
from argparse import ArgumentParser
from datetime import date, datetime, timedelta, timezone
from decimal import Decimal
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import text

from app.core.database import SessionLocal, engine
from app.core.security import hash_password
from app.models.company import Company
from app.models.conversation import Conversation
from app.models.customer import Customer
from app.models.message import Message
from app.models.offer import Offer
from app.models.user import User

SEED_PASSWORD = "Sellince123!"

COMPANIES = [
    {"name": "Orange", "sector": "telecom", "subscription_tier": "standard", "created_days_ago": 45},
    {"name": "Zain", "sector": "telecom", "subscription_tier": "pilot", "created_days_ago": 40},
]

USERS = [
    {"company": "Orange", "full_name": "Ahmad Mansour", "email": "ahmad@orange.com", "role": "admin"},
    {"company": "Orange", "full_name": "Rania Khalil", "email": "rania@orange.com", "role": "agent"},
    {"company": "Zain", "full_name": "Omar Sami", "email": "omar@zain.com", "role": "admin"},
    {"company": "Zain", "full_name": "Fatima Yousef", "email": "fatima@zain.com", "role": "agent"},
]

CUSTOMERS = [
    {"company": "Orange", "name": "Ahmed Al-Fayez", "phone": "0791111111", "current_plan": "20GB Data Plan", "usage_percentage": "92.00", "contract_end_date": "2026-12-31", "segment": "Heavy User"},
    {"company": "Orange", "name": "Layla Hassan", "phone": "0792222222", "current_plan": "10GB Data Plan", "usage_percentage": "45.00", "contract_end_date": "2027-06-30", "segment": "Average User"},
    {"company": "Orange", "name": "Omar Khaled", "phone": "0793333333", "current_plan": "Prepaid Plan", "usage_percentage": "15.00", "contract_end_date": None, "segment": "Low Active"},
    {"company": "Zain", "name": "Noor Ibrahim", "phone": "0794444444", "current_plan": "50GB Data Plan", "usage_percentage": "78.00", "contract_end_date": "2026-09-15", "segment": "Heavy User"},
    {"company": "Zain", "name": "Sara Ali", "phone": "0795555555", "current_plan": "5GB Data Plan", "usage_percentage": "95.00", "contract_end_date": "2026-11-30", "segment": "Heavy User"},
]

LARGE_EXTRAS = [
    {"company": "Orange", "name": "Ali Hassan", "phone": "0796666666", "current_plan": "30GB Data Plan", "usage_percentage": "90.00", "contract_end_date": "2027-02-28", "segment": "Heavy User"},
    {"company": "Orange", "name": "Mona Adel", "phone": "0797777777", "current_plan": "10GB Data Plan", "usage_percentage": "40.00", "contract_end_date": "2026-10-31", "segment": "Average User"},
    {"company": "Zain", "name": "Tariq Nasser", "phone": "0798888888", "current_plan": "20GB Data Plan", "usage_percentage": "70.00", "contract_end_date": "2027-04-30", "segment": "Heavy User"},
]

# Indexes into CUSTOMERS per --scale; "large" also appends LARGE_EXTRAS.
SCALE_CUSTOMER_INDEXES = {
    "small": [0, 1, 3],
    "medium": [0, 1, 2, 3, 4],
    "large": [0, 1, 2, 3, 4],
}

# Per customer: conversation + message thread + optional offer.
# Message text templates can reference {usage} (int) and {plan} (customer's current plan).
SCENARIOS = {
    "Ahmed Al-Fayez": {
        "status": "open",
        "started_days_ago": 5,
        "closed_after_hours": None,
        "messages": [
            ("customer", "I keep running out of data every month, it's frustrating.", 0),
            ("ai_agent", "Hi Ahmed, I can see you've used {usage}% of your {plan}. Would you like to see an upgrade option?", 5),
            ("customer", "Yes, what do you recommend?", 20),
            ("system", "Offer sent to customer.", 25),
        ],
        "offer": {"product_name": "50GB Data Plan", "price": "25.00", "status": "sent", "hours_after_start": 1, "confirm_days_after": None},
    },
    "Layla Hassan": {
        "status": "closed",
        "started_days_ago": 12,
        "closed_after_hours": 60,
        "messages": [
            ("customer", "Hi, my contract is ending soon and I need a bigger plan.", 0),
            ("ai_agent", "Hi Layla, you're at {usage}% of your {plan}. Upgrading to a 20GB plan costs $10/month - shall I arrange it?", 5),
            ("customer", "Sounds good, please go ahead.", 30),
            ("system", "Customer accepted offer - upgrade activated.", 35),
        ],
        "offer": {"product_name": "20GB Data Plan", "price": "10.00", "status": "accepted", "hours_after_start": 1, "confirm_days_after": 1},
    },
    "Omar Khaled": {
        "status": "closed",
        "started_days_ago": 10,
        "closed_after_hours": 6,
        "messages": [
            ("customer", "I'm happy with my prepaid plan for now.", 0),
            ("ai_agent", "No problem, Omar. If your data needs change, we have plans from $10/month.", 3),
            ("system", "Customer declined the offer.", 8),
        ],
        "offer": {"product_name": "20GB Data Plan", "price": "10.00", "status": "declined", "hours_after_start": 1, "confirm_days_after": None},
    },
    "Noor Ibrahim": {
        "status": "open",
        "started_days_ago": 3,
        "closed_after_hours": None,
        "messages": [
            ("customer", "Do you think I should move to a premium plan?", 0),
            ("ai_agent", "Noor, you're at {usage}% of your {plan}. The 100GB Premium Plan at $45 keeps you fully covered with priority support.", 4),
            ("customer", "OK, let's do it.", 25),
            ("system", "Offer accepted by customer.", 30),
        ],
        "offer": {"product_name": "100GB Premium Plan", "price": "45.00", "status": "accepted", "hours_after_start": 1, "confirm_days_after": 2},
    },
    "Sara Ali": {
        "status": "open",
        "started_days_ago": 1,
        "closed_after_hours": None,
        "messages": [
            ("customer", "I keep hitting my data cap before the month ends.", 0),
            ("ai_agent", "Sara, you've used {usage}% of your {plan}. The 100GB Premium Plan for $45 would cover you with room to spare.", 5),
            ("customer", "Interesting - tell me more.", 40),
            ("system", "Offer sent to customer.", 45),
        ],
        "offer": {"product_name": "100GB Premium Plan", "price": "45.00", "status": "sent", "hours_after_start": 2, "confirm_days_after": None},
    },
    "Ali Hassan": {
        "status": "open",
        "started_days_ago": 4,
        "closed_after_hours": None,
        "messages": [
            ("customer", "My team burns through hotspot data fast.", 0),
            ("ai_agent", "Ali, you're at {usage}% of your {plan}. The 50GB Data Plan for $25 keeps everyone online.", 6),
            ("customer", "Alright, what's the price?", 30),
            ("system", "Offer sent to customer.", 35),
        ],
        "offer": {"product_name": "50GB Data Plan", "price": "25.00", "status": "sent", "hours_after_start": 1, "confirm_days_after": None},
    },
    "Mona Adel": {
        "status": "closed",
        "started_days_ago": 8,
        "closed_after_hours": 30,
        "messages": [
            ("customer", "I just wanted to ask about my bill.", 0),
            ("ai_agent", "Mona, I can see you're at {usage}% of your {plan}. Anything else I can help with?", 3),
            ("customer", "No, that's all. Thanks!", 10),
            ("system", "Conversation closed.", 15),
        ],
        "offer": None,
    },
    "Tariq Nasser": {
        "status": "open",
        "started_days_ago": 2,
        "closed_after_hours": None,
        "messages": [
            ("customer", "Is there a plan with more data for streaming?", 0),
            ("ai_agent", "Tariq, you're at {usage}% of your {plan}. The 100GB Premium Plan at $45 is great for streaming.", 5),
            ("customer", "Send me the details.", 25),
            ("system", "Offer sent to customer.", 30),
        ],
        "offer": {"product_name": "100GB Premium Plan", "price": "45.00", "status": "sent", "hours_after_start": 1, "confirm_days_after": None},
    },
}


def _now():
    return datetime.now(timezone.utc).replace(tzinfo=None)


def _to_date(value):
    return date.fromisoformat(value) if value else None


def _get_or_create(session, model, defaults, **filters):
    obj = session.query(model).filter_by(**filters).first()
    if obj is None:
        obj = model(**filters, **defaults)
        session.add(obj)
        session.flush()
        return obj, True
    return obj, False


def reset_database():
    with engine.begin() as conn:
        conn.execute(text(
            "TRUNCATE TABLE refresh_tokens, messages, offers, conversations, "
            "customers, users, companies RESTART IDENTITY CASCADE"
        ))
    print("TRUNCATED all app tables (RESTART IDENTITY CASCADE); ids will restart at 1.")


def _customers_for(scale):
    customers = [CUSTOMERS[i] for i in SCALE_CUSTOMER_INDEXES[scale]]
    if scale == "large":
        customers.extend(LARGE_EXTRAS)
    return customers


def print_summary(session):
    counts = [
        ("companies", session.query(Company).count()),
        ("users", session.query(User).count()),
        ("customers", session.query(Customer).count()),
        ("conversations", session.query(Conversation).count()),
        ("messages", session.query(Message).count()),
        ("offers", session.query(Offer).count()),
    ]
    print("\nSeed data completed successfully!\n")
    print(f"  {'table':<16} count")
    print(f"  {'-'*24}")
    for table, count in counts:
        print(f"  {table:<16} {count}")
    print(f"\n  Demo logins (shared password: {SEED_PASSWORD}):")
    for user_data in USERS:
        print(f"    {user_data['email']:<25} ({user_data['role']})")


def seed(scale="medium", reset=False):
    now = _now()
    if reset:
        reset_database()

    session = SessionLocal()
    try:
        password_hash = hash_password(SEED_PASSWORD)

        company_by_name = {}
        for company_data in COMPANIES:
            company, created = _get_or_create(
                session,
                Company,
                {
                    "sector": company_data["sector"],
                    "subscription_tier": company_data["subscription_tier"],
                    "created_at": now - timedelta(days=company_data["created_days_ago"]),
                },
                name=company_data["name"],
            )
            company_by_name[company.name] = company
            status = "created" if created else "exists"
            print(f"  company  {status:7s} {company.name:<8} {company.sector}/{company.subscription_tier}")

        for user_data in USERS:
            company = company_by_name[user_data["company"]]
            user, created = _get_or_create(
                session,
                User,
                {
                    "company_id": company.id,
                    "full_name": user_data["full_name"],
                    "password_hash": password_hash,
                    "role": user_data["role"],
                    "created_at": now - timedelta(days=38),
                },
                email=user_data["email"],
            )
            status = "created" if created else "exists"
            print(f"  user     {status:7s} {user.email:<25} {user_data['role']}")

        customers = []
        for customer_data in _customers_for(scale):
            company = company_by_name[customer_data["company"]]
            customer, created = _get_or_create(
                session,
                Customer,
                {
                    "current_plan": customer_data["current_plan"],
                    "usage_percentage": Decimal(customer_data["usage_percentage"]),
                    "contract_end_date": _to_date(customer_data["contract_end_date"]),
                    "segment": customer_data["segment"],
                    "created_at": now - timedelta(days=30),
                },
                company_id=company.id,
                name=customer_data["name"],
                phone=customer_data["phone"],
            )
            customers.append(customer)
            status = "created" if created else "exists"
            print(f"  customer {status:7s} {customer.name:<18} {company.name} ({customer.segment})")

        for customer in customers:
            scenario = SCENARIOS[customer.name]
            started_at = now - timedelta(days=scenario["started_days_ago"], hours=6)
            closed_at = (
                started_at + timedelta(hours=scenario["closed_after_hours"])
                if scenario["closed_after_hours"] else None
            )
            conversation, conv_created = _get_or_create(
                session,
                Conversation,
                {
                    "company_id": customer.company_id,
                    "status": scenario["status"],
                    "started_at": started_at,
                    "closed_at": closed_at,
                },
                customer_id=customer.id,
            )
            if conv_created:
                print(f"  conv     created   {customer.name:<18} status={conversation.status}")
                for sender, template, minutes_after in scenario["messages"]:
                    _get_or_create(
                        session,
                        Message,
                        {"sent_at": started_at + timedelta(minutes=minutes_after)},
                        conversation_id=conversation.id,
                        sender=sender,
                        text=template.format(usage=int(customer.usage_percentage), plan=customer.current_plan),
                    )

            offer_data = scenario.get("offer")
            if offer_data:
                offer_created_at = started_at + timedelta(hours=offer_data["hours_after_start"])
                confirmed_at = (
                    offer_created_at + timedelta(days=offer_data["confirm_days_after"])
                    if offer_data["confirm_days_after"] else None
                )
                offer, created = _get_or_create(
                    session,
                    Offer,
                    {
                        "conversation_id": conversation.id,
                        "company_id": customer.company_id,
                        "price": Decimal(offer_data["price"]),
                        "status": offer_data["status"],
                        "created_at": offer_created_at,
                        "confirmed_at": confirmed_at,
                    },
                    customer_id=customer.id,
                    product_name=offer_data["product_name"],
                )
                if created:
                    print(f"  offer    created   {offer.product_name:<22} ({offer.status}) for {customer.name}")

        session.commit()
        print_summary(session)
    except Exception as e:
        session.rollback()
        print(f"Seeding failed: {e}")
        raise
    finally:
        session.close()


def main():
    parser = ArgumentParser(description="Seed Sellince demo data (default: idempotent upsert).")
    parser.add_argument(
        "--reset",
        action="store_true",
        help="TRUNCATE all app tables (RESTART IDENTITY CASCADE) before seeding.",
    )
    parser.add_argument(
        "--scale",
        choices=["small", "medium", "large"],
        default="medium",
        help="Amount of demo data to seed.",
    )
    args = parser.parse_args()
    seed(scale=args.scale, reset=args.reset)


if __name__ == "__main__":
    main()