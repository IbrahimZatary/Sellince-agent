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
    # ---- Orange (15) - exact rows from archive/Mock_Customer_Data.pdf ----
    # mobile data users (1-10)
    {"company": "Orange", "name": "Ahmed Al-Fayez", "phone": "0791111111", "service_type": "mobile_data", "current_plan": "20GB Mobile Data", "speed": "4G", "usage_percentage": "92.00", "contract_end_date": "2026-12-31", "segment": "Heavy User", "interests": "5G, Streaming", "location": None},
    {"company": "Orange", "name": "Layla Hassan", "phone": "0792222222", "service_type": "mobile_data", "current_plan": "10GB Mobile Data", "speed": "4G", "usage_percentage": "45.00", "contract_end_date": "2027-06-30", "segment": "Average User", "interests": "Social Media", "location": None},
    {"company": "Orange", "name": "Omar Khaled", "phone": "0793333333", "service_type": "mobile_data", "current_plan": "5GB Mobile Data", "speed": "4G", "usage_percentage": "15.00", "contract_end_date": "2026-10-15", "segment": "Low User", "interests": None, "location": None},
    {"company": "Orange", "name": "Noor Ibrahim", "phone": "0794444444", "service_type": "mobile_data", "current_plan": "50GB Mobile Data", "speed": "5G", "usage_percentage": "78.00", "contract_end_date": "2026-09-15", "segment": "Heavy User", "interests": "Gaming, 5G", "location": None},
    {"company": "Orange", "name": "Sara Ali", "phone": "0795555555", "service_type": "mobile_data", "current_plan": "5GB Mobile Data", "speed": "4G", "usage_percentage": "95.00", "contract_end_date": "2026-11-30", "segment": "Heavy User", "interests": "Streaming", "location": None},
    {"company": "Orange", "name": "Rana Khoury", "phone": "0796666666", "service_type": "mobile_data", "current_plan": "20GB Mobile Data", "speed": "4G", "usage_percentage": "30.00", "contract_end_date": "2027-03-31", "segment": "Average User", "interests": None, "location": None},
    {"company": "Orange", "name": "Hadi Shahin", "phone": "0797777777", "service_type": "mobile_data", "current_plan": "10GB Mobile Data", "speed": "4G", "usage_percentage": "88.00", "contract_end_date": "2026-10-31", "segment": "Heavy User", "interests": "Phones", "location": None},
    {"company": "Orange", "name": "Dina Salameh", "phone": "0798888888", "service_type": "mobile_data", "current_plan": "5GB Mobile Data", "speed": "4G", "usage_percentage": "60.00", "contract_end_date": "2027-01-15", "segment": "Average User", "interests": "Social Media", "location": None},
    {"company": "Orange", "name": "Sami Jaber", "phone": "0799999999", "service_type": "mobile_data", "current_plan": "20GB Mobile Data", "speed": "4G", "usage_percentage": "12.00", "contract_end_date": "2027-05-20", "segment": "Low User", "interests": None, "location": None},
    {"company": "Orange", "name": "Lina Qasim", "phone": "0790000000", "service_type": "mobile_data", "current_plan": "50GB Mobile Data", "speed": "5G", "usage_percentage": "85.00", "contract_end_date": "2026-08-31", "segment": "Heavy User", "interests": "5G, Gaming", "location": None},
    # fiber home internet users (11-15)
    {"company": "Orange", "name": "Ahmad Zytoon", "phone": "0781111111", "service_type": "fiber_home", "current_plan": "Fiber 100 Mbps", "speed": "100 Mbps", "usage_percentage": "70.00", "contract_end_date": "2027-02-28", "segment": "Heavy User", "interests": None, "location": "Amman - Abdoun"},
    {"company": "Orange", "name": "Amal Dajah", "phone": "0782222222", "service_type": "fiber_home", "current_plan": "Fiber 50 Mbps", "speed": "50 Mbps", "usage_percentage": "90.00", "contract_end_date": "2026-09-30", "segment": "Heavy User", "interests": None, "location": "Amman - Sweifieh"},
    {"company": "Orange", "name": "Khaled Abu Ali", "phone": "0783333333", "service_type": "fiber_home", "current_plan": "Fiber 30 Mbps", "speed": "30 Mbps", "usage_percentage": "40.00", "contract_end_date": "2027-04-15", "segment": "Average User", "interests": None, "location": "Amman - Jabal Amman"},
    {"company": "Orange", "name": "Nadia Ashour", "phone": "0784444444", "service_type": "fiber_home", "current_plan": "Fiber 100 Mbps", "speed": "100 Mbps", "usage_percentage": "95.00", "contract_end_date": "2026-12-01", "segment": "Heavy User", "interests": None, "location": "Amman - Khalda"},
    {"company": "Orange", "name": "Youssef Haddad", "phone": "0785555555", "service_type": "fiber_home", "current_plan": "Fiber 50 Mbps", "speed": "50 Mbps", "usage_percentage": "25.00", "contract_end_date": "2027-07-01", "segment": "Low User", "interests": None, "location": "Zarqa"},
    # ---- Zain (5) - invented to give trigger 2 coverage + close isolation gaps ----
    {"company": "Zain", "name": "Farah Nasser", "phone": "0790123456", "service_type": "mobile_data", "current_plan": "20GB Mobile Data", "speed": "4G", "usage_percentage": "55.00", "contract_end_date": "2027-09-30", "segment": "Average User", "interests": "5G", "location": None},
    {"company": "Zain", "name": "Hana Khoury", "phone": "0791234567", "service_type": "mobile_data", "current_plan": "10GB Mobile Data", "speed": "4G", "usage_percentage": "30.00", "contract_end_date": "2026-09-26", "segment": "Average User", "interests": None, "location": None},
    {"company": "Zain", "name": "Mahmoud Ezat", "phone": "0792345678", "service_type": "fiber_home", "current_plan": "Fiber 100 Mbps", "speed": "100 Mbps", "usage_percentage": "92.00", "contract_end_date": "2027-04-10", "segment": "Heavy User", "interests": None, "location": "Amman - Sweifieh"},
    {"company": "Zain", "name": "Rania Masri", "phone": "0793456789", "service_type": "mobile_data", "current_plan": "20GB Mobile Data", "speed": "4G", "usage_percentage": "97.00", "contract_end_date": "2027-11-11", "segment": "Heavy User", "interests": None, "location": None},
    {"company": "Zain", "name": "Tamer Saliba", "phone": "0794567890", "service_type": "mobile_data", "current_plan": "5GB Mobile Data", "speed": "4G", "usage_percentage": "40.00", "contract_end_date": "2027-05-15", "segment": "Average User", "interests": None, "location": None},
]

LARGE_EXTRAS = []

# Indexes into CUSTOMERS per --scale; "large" also appends LARGE_EXTRAS.
# small = one case per coverable trigger kind + a no-trigger control (cross-sell
# is intentionally absent everywhere until the AI team defines a "fiber area").
SCALE_CUSTOMER_INDEXES = {
    "small": [0, 3, 13, 15, 16, 19],
    "medium": list(range(20)),
    "large": list(range(20)),
}

# Per customer: conversation + message thread + optional offer.
# Message text templates can reference {usage} (int), {plan} (current plan) and {name}.
# Offer product_names use the use-case catalog from archive/Mock_Customer_Data.pdf.
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
        "offer": {"product_name": "50GB Mobile 5G", "price": "25.00", "status": "sent", "hours_after_start": 1, "confirm_days_after": None},
    },
    "Omar Khaled": {
        "status": "closed",
        "started_days_ago": 10,
        "closed_after_hours": 6,
        "messages": [
            ("customer", "I'm happy with my current plan for now.", 0),
            ("ai_agent", "No problem, Omar. If your needs change, we have plans from 8 JOD/month.", 3),
            ("system", "Customer declined the offer.", 8),
        ],
        "offer": {"product_name": "20GB Mobile 4G", "price": "15.00", "status": "declined", "hours_after_start": 1, "confirm_days_after": None},
    },
    "Noor Ibrahim": {
        "status": "open",
        "started_days_ago": 3,
        "closed_after_hours": None,
        "messages": [
            ("customer", "Do you think I should move to a 5G plan?", 0),
            ("ai_agent", "Noor, you're at {usage}% of your {plan} and your contract ends soon. The 50GB Mobile 5G at 25 JOD keeps you fully covered.", 4),
            ("customer", "OK, let's do it.", 25),
            ("system", "Offer accepted by customer.", 30),
        ],
        "offer": {"product_name": "50GB Mobile 5G", "price": "25.00", "status": "accepted", "hours_after_start": 1, "confirm_days_after": 2},
    },
    "Lina Qasim": {
        "status": "closed",
        "started_days_ago": 12,
        "closed_after_hours": 20,
        "messages": [
            ("customer", "My contract ended and I lost my plan benefits.", 0),
            ("ai_agent", "Lina, we kept your {plan} running and can renew it at 25 JOD.", 3),
            ("customer", "Renew it please.", 15),
            ("system", "Customer accepted the retention offer.", 20),
        ],
        "offer": {"product_name": "50GB Mobile 5G", "price": "25.00", "status": "accepted", "hours_after_start": 1, "confirm_days_after": 1},
    },
    "Amal Dajah": {
        "status": "open",
        "started_days_ago": 4,
        "closed_after_hours": None,
        "messages": [
            ("customer", "My fiber is getting slow with everyone at home online.", 0),
            ("ai_agent", "Amal, you're at {usage}% of your {plan}. Upgrading to Fiber 100 Mbps at 35 JOD would smooth things out.", 5),
            ("customer", "Alright, what's the price?", 25),
            ("system", "Offer sent to customer.", 30),
        ],
        "offer": {"product_name": "Fiber 100 Mbps", "price": "35.00", "status": "sent", "hours_after_start": 1, "confirm_days_after": None},
    },
    "Farah Nasser": {
        "status": "open",
        "started_days_ago": 2,
        "closed_after_hours": None,
        "messages": [
            ("customer", "Is 5G worth upgrading to?", 0),
            ("ai_agent", "Farah, with your interest in 5G, the 5G Add-on at 5 JOD gives you a 5G speed boost on your current plan.", 5),
            ("customer", "Send me the details.", 20),
            ("system", "Offer sent to customer.", 25),
        ],
        "offer": {"product_name": "5G Add-on", "price": "5.00", "status": "sent", "hours_after_start": 1, "confirm_days_after": None},
    },
    "Hana Khoury": {
        "status": "open",
        "started_days_ago": 1,
        "closed_after_hours": None,
        "messages": [
            ("customer", "My contract is ending soon, what options do I have?", 0),
            ("ai_agent", "Hana, your {plan} is expiring soon. Renew and step up to 20GB Mobile 4G at 15 JOD with a renewal discount.", 5),
            ("customer", "Sounds good.", 18),
            ("system", "Offer sent to customer.", 25),
        ],
        "offer": {"product_name": "20GB Mobile 4G", "price": "15.00", "status": "sent", "hours_after_start": 1, "confirm_days_after": None},
    },
    "Mahmoud Ezat": {
        "status": "open",
        "started_days_ago": 2,
        "closed_after_hours": None,
        "messages": [
            ("customer", "Can you check if I can get a faster fiber connection?", 0),
            ("ai_agent", "Mahmoud, you're at {usage}% of your {plan}. Fiber 100 Mbps at 35 JOD is the next step up.", 5),
            ("customer", "Let's go ahead.", 15),
            ("system", "Offer sent to customer.", 20),
        ],
        "offer": {"product_name": "Fiber 100 Mbps", "price": "35.00", "status": "sent", "hours_after_start": 1, "confirm_days_after": None},
    },
    "Rania Masri": {
        "status": "open",
        "started_days_ago": 1,
        "closed_after_hours": None,
        "messages": [
            ("customer", "I'm burning through data faster than ever.", 0),
            ("ai_agent", "Rania, you've used {usage}% of your {plan}. The 50GB Mobile 5G at 25 JOD would cover you.", 5),
            ("customer", "Send it over.", 20),
            ("system", "Offer sent to customer.", 25),
        ],
        "offer": {"product_name": "50GB Mobile 5G", "price": "25.00", "status": "sent", "hours_after_start": 1, "confirm_days_after": None},
    },
    "Tamer Saliba": {
        "status": "closed",
        "started_days_ago": 6,
        "closed_after_hours": 24,
        "messages": [
            ("customer", "Just want to confirm my balance please.", 0),
            ("ai_agent", "Tamer, I can see you're at {usage}% of your {plan}. You're all set - anything else?", 3),
            ("customer", "All good, thanks!", 8),
            ("system", "Conversation closed.", 12),
        ],
        "offer": None,
    },
}


def _scenario_for(customer):
    """Return a scenario for any customer; unknown names fall back to a default."""
    name = customer["name"]
    if name in SCENARIOS:
        return SCENARIOS[name]
    return {
        "status": "open",
        "started_days_ago": 3,
        "closed_after_hours": None,
        "messages": [
            ("customer", "I'd like to check my {plan} usage.", 0),
            ("ai_agent", "Hi {name}, you're at {usage}% of your {plan}. Is there anything I can help you with?", 5),
            ("system", "Conversation logged.", 45),
        ],
        "offer": None,
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
                    "service_type": customer_data["service_type"],
                    "speed": customer_data["speed"],
                    "usage_percentage": Decimal(customer_data["usage_percentage"]),
                    "contract_end_date": _to_date(customer_data["contract_end_date"]),
                    "segment": customer_data["segment"],
                    "interests": customer_data["interests"],
                    "location": customer_data["location"],
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
            scenario = _scenario_for({"name": customer.name})
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
                        text=template.format(name=customer.name, usage=int(customer.usage_percentage), plan=customer.current_plan),
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