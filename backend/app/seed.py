"""Demo data seed for the Sellince backend.

Snapshot of the live DB as of 2026-09-22 (2 companies, 4 users,
20 customers, 13 conversations, 42 messages, 8 offers, 6 attributions).

Run from the ``backend/`` directory:

    python3 -m app.seed --reset    # TRUNCATE all tables, then seed the exact snapshot fresh
    python3 -m app.seed            # idempotent upsert by ID to the exact snapshot state

NOTE: ``--scale`` is accepted for backwards compatibility but ignored;
the seed always reproduces the full snapshot above.
"""

import sys
from argparse import ArgumentParser
from datetime import datetime
from decimal import Decimal
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import text

from app.core.database import SessionLocal, engine
from app.core.security import hash_password
from app.models.company import Company
from app.models.conversation import Conversation
from app.models.customer import Customer
from app.models.attribution import Attribution
from app.models.message import Message
from app.models.offer import Offer
from app.models.user import User

SEED_PASSWORD = "Sellince123!"


def _dt(value):
    return datetime.fromisoformat(value) if value else None


def _date(value):
    return _dt(value).date() if value else None


SNAPSHOT_COMPANIES = [
    {"id": 1, "name": "Orange", "sector": "telecom", "subscription_tier": "standard", "created_at": "2026-08-08 12:41:13.742967"},
    {"id": 2, "name": "Zain", "sector": "telecom", "subscription_tier": "pilot", "created_at": "2026-08-13 12:41:13.742967"},
]

SNAPSHOT_USERS = [
    {"id": 1, "company_id": 1, "full_name": "Ahmad Mansour", "email": "ahmad@orange.com", "role": "admin", "created_at": "2026-08-15 12:41:13.742967"},
    {"id": 2, "company_id": 1, "full_name": "Rania Khalil", "email": "rania@orange.com", "role": "agent", "created_at": "2026-08-15 12:41:13.742967"},
    {"id": 3, "company_id": 2, "full_name": "Omar Sami", "email": "omar@zain.com", "role": "admin", "created_at": "2026-08-15 12:41:13.742967"},
    {"id": 4, "company_id": 2, "full_name": "Fatima Yousef", "email": "fatima@zain.com", "role": "agent", "created_at": "2026-08-15 12:41:13.742967"},
]

SNAPSHOT_CUSTOMERS = [
    {"id": 1, "company_id": 1, "name": "Ahmed Al-Fayez", "phone": "0781111111", "current_plan": "50GB Mobile 5G", "service_type": "mobile_data", "speed": "4G", "usage_percentage": "0.00", "contract_end_date": "2026-12-31", "segment": "Heavy User", "interests": "5G, Streaming", "location": None, "created_at": "2026-08-23 12:41:13.742967"},
    {"id": 2, "company_id": 1, "name": "Layla Hassan", "phone": "0782222222", "current_plan": "10GB Mobile Data", "service_type": "mobile_data", "speed": "4G", "usage_percentage": "45.00", "contract_end_date": "2026-09-25", "segment": "Average User", "interests": "Social Media", "location": None, "created_at": "2026-08-23 12:41:13.742967"},
    {"id": 3, "company_id": 1, "name": "Omar Khaled", "phone": "0783333333", "current_plan": "5GB Mobile Data", "service_type": "mobile_data", "speed": "4G", "usage_percentage": "15.00", "contract_end_date": "2026-10-15", "segment": "Low User", "interests": None, "location": None, "created_at": "2026-08-23 12:41:13.742967"},
    {"id": 4, "company_id": 1, "name": "Noor Ibrahim", "phone": "0784444444", "current_plan": "20GB Mobile 4G", "service_type": "mobile_data", "speed": "5G", "usage_percentage": "0.00", "contract_end_date": "2026-09-15", "segment": "Heavy User", "interests": "Gaming, 5G", "location": None, "created_at": "2026-08-23 12:41:13.742967"},
    {"id": 5, "company_id": 1, "name": "Sara Ali", "phone": "0785555555", "current_plan": "20GB Mobile 4G", "service_type": "mobile_data", "speed": "4G", "usage_percentage": "0.00", "contract_end_date": "2026-11-30", "segment": "Heavy User", "interests": "Streaming", "location": None, "created_at": "2026-08-23 12:41:13.742967"},
    {"id": 6, "company_id": 1, "name": "Rana Khoury", "phone": "0786666666", "current_plan": "20GB Mobile Data", "service_type": "mobile_data", "speed": "4G", "usage_percentage": "30.00", "contract_end_date": "2027-03-31", "segment": "Average User", "interests": None, "location": None, "created_at": "2026-08-23 12:41:13.742967"},
    {"id": 7, "company_id": 1, "name": "Hadi Shahin", "phone": "0787777777", "current_plan": "20GB Mobile 4G", "service_type": "mobile_data", "speed": "4G", "usage_percentage": "0.00", "contract_end_date": "2026-09-28", "segment": "Heavy User", "interests": "Phones", "location": None, "created_at": "2026-08-23 12:41:13.742967"},
    {"id": 8, "company_id": 1, "name": "Dina Salameh", "phone": "0788888888", "current_plan": "5GB Mobile Data", "service_type": "mobile_data", "speed": "4G", "usage_percentage": "60.00", "contract_end_date": "2027-01-15", "segment": "Average User", "interests": "Social Media", "location": None, "created_at": "2026-08-23 12:41:13.742967"},
    {"id": 9, "company_id": 1, "name": "Sami Jaber", "phone": "0789999999", "current_plan": "20GB Mobile Data", "service_type": "mobile_data", "speed": "4G", "usage_percentage": "12.00", "contract_end_date": "2027-05-20", "segment": "Low User", "interests": None, "location": None, "created_at": "2026-08-23 12:41:13.742967"},
    {"id": 10, "company_id": 1, "name": "Lina Qasim", "phone": "0780000000", "current_plan": "50GB Mobile Data", "service_type": "mobile_data", "speed": "5G", "usage_percentage": "85.00", "contract_end_date": "2026-08-31", "segment": "Heavy User", "interests": "5G, Gaming", "location": None, "created_at": "2026-08-23 12:41:13.742967"},
    {"id": 11, "company_id": 1, "name": "Ahmad Zytoon", "phone": "0780111111", "current_plan": "Fiber 100 Mbps", "service_type": "fiber_home", "speed": "100 Mbps", "usage_percentage": "90.00", "contract_end_date": "2027-02-28", "segment": "Heavy User", "interests": None, "location": "Amman - Abdoun", "created_at": "2026-08-23 12:41:13.742967"},
    {"id": 12, "company_id": 1, "name": "Amal Dajah", "phone": "0780222222", "current_plan": "Fiber 100 Mbps", "service_type": "fiber_home", "speed": "50 Mbps", "usage_percentage": "0.00", "contract_end_date": "2026-09-30", "segment": "Heavy User", "interests": None, "location": "Amman - Sweifieh", "created_at": "2026-08-23 12:41:13.742967"},
    {"id": 13, "company_id": 1, "name": "Khaled Abu Ali", "phone": "0780333333", "current_plan": "Fiber 50 Mbps", "service_type": "fiber_home", "speed": "30 Mbps", "usage_percentage": "0.00", "contract_end_date": "2026-09-28", "segment": "Average User", "interests": None, "location": "Amman - Jabal Amman", "created_at": "2026-08-23 12:41:13.742967"},
    {"id": 14, "company_id": 1, "name": "Nadia Ashour", "phone": "0780444444", "current_plan": "Fiber 100 Mbps", "service_type": "fiber_home", "speed": "100 Mbps", "usage_percentage": "95.00", "contract_end_date": "2026-12-01", "segment": "Heavy User", "interests": None, "location": "Amman - Khalda", "created_at": "2026-08-23 12:41:13.742967"},
    {"id": 15, "company_id": 1, "name": "Youssef Haddad", "phone": "0780555555", "current_plan": "Fiber 50 Mbps", "service_type": "fiber_home", "speed": "50 Mbps", "usage_percentage": "25.00", "contract_end_date": "2026-09-25", "segment": "Low User", "interests": None, "location": "Zarqa", "created_at": "2026-08-23 12:41:13.742967"},
    {"id": 16, "company_id": 2, "name": "Farah Nasser", "phone": "0790123456", "current_plan": "20GB Mobile Data", "service_type": "mobile_data", "speed": "4G", "usage_percentage": "55.00", "contract_end_date": "2027-09-30", "segment": "Average User", "interests": "5G", "location": None, "created_at": "2026-08-23 12:41:13.742967"},
    {"id": 17, "company_id": 2, "name": "Hana Khoury", "phone": "0791234567", "current_plan": "10GB Mobile Data", "service_type": "mobile_data", "speed": "4G", "usage_percentage": "30.00", "contract_end_date": "2026-09-26", "segment": "Average User", "interests": None, "location": None, "created_at": "2026-08-23 12:41:13.742967"},
    {"id": 18, "company_id": 2, "name": "Mahmoud Ezat", "phone": "0792345678", "current_plan": "Fiber 100 Mbps", "service_type": "fiber_home", "speed": "100 Mbps", "usage_percentage": "92.00", "contract_end_date": "2027-04-10", "segment": "Heavy User", "interests": None, "location": "Amman - Sweifieh", "created_at": "2026-08-23 12:41:13.742967"},
    {"id": 19, "company_id": 2, "name": "Rania Masri", "phone": "0793456789", "current_plan": "20GB Mobile Data", "service_type": "mobile_data", "speed": "4G", "usage_percentage": "97.00", "contract_end_date": "2027-11-11", "segment": "Heavy User", "interests": None, "location": None, "created_at": "2026-08-23 12:41:13.742967"},
    {"id": 20, "company_id": 2, "name": "Tamer Saliba", "phone": "0794567890", "current_plan": "Prepaid Plan", "service_type": "mobile_data", "speed": "4G", "usage_percentage": "60.00", "contract_end_date": "2027-05-15", "segment": "Heavy User", "interests": None, "location": None, "created_at": "2026-08-23 12:41:13.742967"},
]

SNAPSHOT_CONVERSATIONS = [
    {"id": 2, "customer_id": 6, "company_id": 1, "status": "open", "started_at": "2026-09-22 13:34:06.577313", "closed_at": None},
    {"id": 3, "customer_id": 8, "company_id": 1, "status": "open", "started_at": "2026-09-22 13:34:15.070926", "closed_at": None},
    {"id": 4, "customer_id": 9, "company_id": 1, "status": "open", "started_at": "2026-09-22 13:34:19.925468", "closed_at": None},
    {"id": 5, "customer_id": 10, "company_id": 1, "status": "open", "started_at": "2026-09-22 13:34:25.101814", "closed_at": None},
    {"id": 6, "customer_id": 3, "company_id": 1, "status": "closed", "started_at": "2026-09-22 13:35:44.464658", "closed_at": "2026-09-22 14:00:00"},
    {"id": 7, "customer_id": 15, "company_id": 1, "status": "closed", "started_at": "2026-09-22 13:36:33.487909", "closed_at": "2026-09-22 14:00:00"},
    {"id": 8, "customer_id": 1, "company_id": 1, "status": "closed", "started_at": "2026-09-22 13:36:44.256009", "closed_at": "2026-09-21 13:00:00"},
    {"id": 9, "customer_id": 5, "company_id": 1, "status": "closed", "started_at": "2026-09-22 13:37:50.609373", "closed_at": "2026-09-21 15:00:00"},
    {"id": 10, "customer_id": 7, "company_id": 1, "status": "closed", "started_at": "2026-09-22 13:38:29.006827", "closed_at": "2026-09-22 13:38:46.837525"},
    {"id": 11, "customer_id": 11, "company_id": 1, "status": "open", "started_at": "2026-09-22 13:38:52.463881", "closed_at": None},
    {"id": 12, "customer_id": 12, "company_id": 1, "status": "closed", "started_at": "2026-09-22 13:39:38.249116", "closed_at": "2026-09-22 13:40:46.778923"},
    {"id": 13, "customer_id": 4, "company_id": 1, "status": "closed", "started_at": "2026-09-22 16:23:38.038803", "closed_at": "2026-09-24 13:00:00"},
    {"id": 14, "customer_id": 13, "company_id": 1, "status": "closed", "started_at": "2026-09-22 16:43:05.834499", "closed_at": "2026-09-22 16:44:09"},
]

SNAPSHOT_MESSAGES = [
    {"id": 3, "conversation_id": 2, "sender": "customer", "text": "Hey", "sent_at": "2026-09-22 13:34:06.577313"},
    {"id": 4, "conversation_id": 2, "sender": "agent", "text": "Hello Rana Khoury, thank you for reaching out. How can we assist you with your account today?", "sent_at": "2026-09-22 13:34:06.577313"},
    {"id": 5, "conversation_id": 3, "sender": "customer", "text": "Heyy", "sent_at": "2026-09-22 13:34:15.070926"},
    {"id": 6, "conversation_id": 3, "sender": "agent", "text": "Hello Dina Salameh, thank you for reaching out. How can we assist you with your account today?", "sent_at": "2026-09-22 13:34:15.070926"},
    {"id": 7, "conversation_id": 4, "sender": "customer", "text": "What do you have for me?", "sent_at": "2026-09-22 13:34:19.925468"},
    {"id": 8, "conversation_id": 4, "sender": "agent", "text": "Hello Sami Jaber, thank you for reaching out. How can we assist you with your account today?", "sent_at": "2026-09-22 13:34:19.925468"},
    {"id": 9, "conversation_id": 5, "sender": "customer", "text": "Hi", "sent_at": "2026-09-22 13:34:25.101814"},
    {"id": 10, "conversation_id": 5, "sender": "agent", "text": "Hello Lina Qasim, thank you for reaching out. How can we assist you with your account today?", "sent_at": "2026-09-22 13:34:25.101814"},
    {"id": 11, "conversation_id": 6, "sender": "customer", "text": "Hey", "sent_at": "2026-09-22 13:35:44.464658"},
    {"id": 12, "conversation_id": 6, "sender": "agent", "text": "Hi Omar Khaled, I see you’re using 15% of your 5 GB plan and your contract is expiring soon—upgrade to our 20 GB Mobile 4G plan for just 15 JOD and enjoy more data and faster speeds.", "sent_at": "2026-09-22 13:35:44.464658"},
    {"id": 13, "conversation_id": 6, "sender": "customer", "text": "No thanks, not interested", "sent_at": "2026-09-22 13:36:26.853932"},
    {"id": 14, "conversation_id": 6, "sender": "agent", "text": "Thank you for letting me know.  \nIf you have any questions about our 20GB Mobile 4G plan, which includes 20GB data and 4G speed, I’m happy to help.  \nFeel free to reach out whenever you’re ready.", "sent_at": "2026-09-22 13:36:26.853932"},
    {"id": 15, "conversation_id": 7, "sender": "customer", "text": "Hey", "sent_at": "2026-09-22 13:36:33.487909"},
    {"id": 16, "conversation_id": 7, "sender": "agent", "text": "Hi Youssef Haddad, your current 50 Mbps Fiber plan is set to expire soon, and we’d love to offer you an upgrade to 100 Mbps for just 35 JOD—double your speed with no extra hassle. Let me know if you’d like to lock in this deal before your contract ends.", "sent_at": "2026-09-22 13:36:33.487909"},
    {"id": 17, "conversation_id": 7, "sender": "customer", "text": "No thanks, not interested", "sent_at": "2026-09-22 13:36:38.729608"},
    {"id": 18, "conversation_id": 7, "sender": "agent", "text": "Thank you for letting me know. The Fiber 100 Mbps plan is priced at 35 JOD. I don’t have a confirmed discount available in the information provided. It includes unlimited data and WiFi.", "sent_at": "2026-09-22 13:36:38.729608"},
    {"id": 19, "conversation_id": 8, "sender": "customer", "text": "Hey", "sent_at": "2026-09-22 13:36:44.256009"},
    {"id": 20, "conversation_id": 8, "sender": "agent", "text": "Hi Ahmed Al‑Fayez, I see you’re already using 92 % of your 20 GB mobile data—upgrade to our 50 GB 5G plan for just 25 JOD and keep your connection smooth and fast. Let me know if you’d like to switch today!", "sent_at": "2026-09-22 13:36:44.256009"},
    {"id": 21, "conversation_id": 8, "sender": "customer", "text": "Okay I want it", "sent_at": "2026-09-22 13:36:53.040854"},
    {"id": 22, "conversation_id": 8, "sender": "agent", "text": "You've selected 50GB Mobile 5G.\nYour selected product includes:\n- 50GB data\n- 5G speed\n- Unlimited calls\n- Streaming", "sent_at": "2026-09-22 13:36:53.040854"},
    {"id": 23, "conversation_id": 9, "sender": "customer", "text": "Hi", "sent_at": "2026-09-22 13:37:50.609373"},
    {"id": 24, "conversation_id": 9, "sender": "agent", "text": "Hi Sara Ali, I see you’re using 95% of your 5 GB mobile data—upgrade to our 20 GB 4G plan for just 15 JOD and enjoy uninterrupted connectivity. Let me know if you’d like to switch!", "sent_at": "2026-09-22 13:37:50.609373"},
    {"id": 25, "conversation_id": 9, "sender": "customer", "text": "I will take it", "sent_at": "2026-09-22 13:38:00.004990"},
    {"id": 26, "conversation_id": 9, "sender": "agent", "text": "You've selected 20GB Mobile 4G.\nYour selected product includes:\n- 20GB data\n- 4G speed\n- Standard calls", "sent_at": "2026-09-22 13:38:00.004990"},
    {"id": 27, "conversation_id": 10, "sender": "customer", "text": "Hey", "sent_at": "2026-09-22 13:38:29.006827"},
    {"id": 28, "conversation_id": 10, "sender": "agent", "text": "Hi Hadi Shahin, I see your 10 GB plan is 88 % used and your contract is about to expire—upgrade to our 20 GB Mobile 4G for just 15 JOD and keep your data flow uninterrupted.", "sent_at": "2026-09-22 13:38:29.006827"},
    {"id": 29, "conversation_id": 10, "sender": "customer", "text": "Alright I will take it", "sent_at": "2026-09-22 13:38:41.223221"},
    {"id": 30, "conversation_id": 10, "sender": "agent", "text": "You've selected 20GB Mobile 4G.\nYour selected product includes:\n- 20GB data\n- 4G speed\n- Standard calls", "sent_at": "2026-09-22 13:38:41.223221"},
    {"id": 31, "conversation_id": 11, "sender": "customer", "text": "Hey", "sent_at": "2026-09-22 13:38:52.463881"},
    {"id": 32, "conversation_id": 11, "sender": "agent", "text": "Hello Ahmad Zytoon, thank you for reaching out. How can we assist you with your account today?", "sent_at": "2026-09-22 13:38:52.463881"},
    {"id": 33, "conversation_id": 12, "sender": "customer", "text": "Hey", "sent_at": "2026-09-22 13:39:38.249116"},
    {"id": 34, "conversation_id": 12, "sender": "agent", "text": "Hi Amal Dajah, I see you’re using 90 % of your 50 Mbps fiber plan—upgrade to 100 Mbps for just 35 JOD and double your speed without extra cost. Let me know if you’d like to switch today!", "sent_at": "2026-09-22 13:39:38.249116"},
    {"id": 35, "conversation_id": 12, "sender": "customer", "text": "Okay I want it", "sent_at": "2026-09-22 13:39:48.270030"},
    {"id": 36, "conversation_id": 12, "sender": "agent", "text": "You've selected Fiber 100 Mbps.\nYour selected product includes:\n- 100 Mbps\n- Unlimited data\n- WiFi", "sent_at": "2026-09-22 13:39:48.270030"},
    {"id": 41, "conversation_id": 13, "sender": "customer", "text": "Hi", "sent_at": "2026-09-22 16:25:02.249381"},
    {"id": 42, "conversation_id": 13, "sender": "agent", "text": "Hi Noor, I see you’re using 95% of your 10 GB plan—upgrade to our 20 GB Mobile 4G for just 15 JOD and enjoy uninterrupted data. Let me know if you’d like to switch today.", "sent_at": "2026-09-22 16:25:02.249381"},
    {"id": 43, "conversation_id": 13, "sender": "customer", "text": "I want it", "sent_at": "2026-09-22 16:25:38.160758"},
    {"id": 44, "conversation_id": 13, "sender": "agent", "text": "You've selected 20GB Mobile 4G.\nYour selected product includes:\n- 20GB data\n- 4G speed\n- Standard calls", "sent_at": "2026-09-22 16:25:38.160758"},
    {"id": 45, "conversation_id": 14, "sender": "customer", "text": "Heyy", "sent_at": "2026-09-22 16:43:05.834499"},
    {"id": 46, "conversation_id": 14, "sender": "agent", "text": "Hi Khaled, as your 30 Mbps Fiber plan is about to expire, we can upgrade you to 50 Mbps Fiber for just 25 JOD/month, giving you faster speeds and more value. Let me know if you'd like to switch.", "sent_at": "2026-09-22 16:43:05.834499"},
    {"id": 47, "conversation_id": 14, "sender": "customer", "text": "Okay, I'll take it", "sent_at": "2026-09-22 16:43:20.893863"},
    {"id": 48, "conversation_id": 14, "sender": "agent", "text": "You've selected Fiber 50 Mbps.\nYour selected product includes:\n- 50 Mbps\n- Unlimited data", "sent_at": "2026-09-22 16:43:20.893863"},
]

SNAPSHOT_OFFERS = [
    {"id": 2, "customer_id": 3, "conversation_id": 6, "company_id": 1, "product_name": "20GB Mobile 4G", "price": "15.00", "status": "declined", "created_at": "2026-09-22 13:36:26.853932", "accepted_at": None},
    {"id": 4, "customer_id": 15, "conversation_id": 7, "company_id": 1, "product_name": "Fiber 100 Mbps", "price": "35.00", "status": "declined", "created_at": "2026-09-22 13:36:38.729608", "accepted_at": None},
    {"id": 6, "customer_id": 1, "conversation_id": 8, "company_id": 1, "product_name": "50GB Mobile 5G", "price": "25.00", "status": "confirmed", "created_at": "2026-09-22 13:36:53.040854", "accepted_at": None},
    {"id": 8, "customer_id": 5, "conversation_id": 9, "company_id": 1, "product_name": "20GB Mobile 4G", "price": "15.00", "status": "confirmed", "created_at": "2026-09-22 13:38:00.004990", "accepted_at": None},
    {"id": 10, "customer_id": 7, "conversation_id": 10, "company_id": 1, "product_name": "20GB Mobile 4G", "price": "15.00", "status": "confirmed", "created_at": "2026-09-22 13:38:41.223221", "accepted_at": None},
    {"id": 12, "customer_id": 12, "conversation_id": 12, "company_id": 1, "product_name": "Fiber 100 Mbps", "price": "35.00", "status": "confirmed", "created_at": "2026-09-22 13:39:48.270030", "accepted_at": None},
    {"id": 14, "customer_id": 4, "conversation_id": 13, "company_id": 1, "product_name": "20GB Mobile 4G", "price": "15.00", "status": "confirmed", "created_at": "2026-09-22 16:25:38.160758", "accepted_at": None},
    {"id": 16, "customer_id": 13, "conversation_id": 14, "company_id": 1, "product_name": "Fiber 50 Mbps", "price": "25.00", "status": "confirmed", "created_at": "2026-09-22 16:43:20.893863", "accepted_at": None},
]

SNAPSHOT_ATTRIBUTIONS = [
    {"id": 1, "conversation_id": 8, "customer_id": 1, "product_id": "1", "product_name": "50GB Mobile 5G", "price": "25.00", "status": "completed", "created_at": "2026-09-21 12:00:00", "confirmed_at": "2026-09-21 13:00:00"},
    {"id": 2, "conversation_id": 9, "customer_id": 5, "product_id": "2", "product_name": "20GB Mobile 4G", "price": "15.00", "status": "completed", "created_at": "2026-09-21 14:00:00", "confirmed_at": "2026-09-21 15:00:00"},
    {"id": 3, "conversation_id": 10, "customer_id": 7, "product_id": "2", "product_name": "20GB Mobile 4G", "price": "15.00", "status": "completed", "created_at": "2026-09-22 13:38:41.223221", "confirmed_at": "2026-09-22 13:38:46.837525"},
    {"id": 4, "conversation_id": 12, "customer_id": 12, "product_id": "4", "product_name": "Fiber 100 Mbps", "price": "35.00", "status": "completed", "created_at": "2026-09-22 13:39:48.270030", "confirmed_at": "2026-09-22 13:40:46.778923"},
    {"id": 5, "conversation_id": 13, "customer_id": 4, "product_id": "2", "product_name": "20GB Mobile 4G", "price": "15.00", "status": "completed", "created_at": "2026-09-24 12:00:00", "confirmed_at": "2026-09-24 13:00:00"},
    {"id": 6, "conversation_id": 14, "customer_id": 13, "product_id": "5", "product_name": "Fiber 50 Mbps", "price": "25.00", "status": "completed", "created_at": "2026-09-22 16:43:20.893863", "confirmed_at": "2026-09-22 16:44:09.302357"},
]


def _upsert(session, model, row_id, values):
    obj = session.get(model, row_id)
    if obj is None:
        obj = model(id=row_id, **values)
        session.add(obj)
    else:
        for key, value in values.items():
            setattr(obj, key, value)
    session.flush()
    return obj


def _reset_sequences():
    try:
        with engine.begin() as conn:
            for table in ("companies", "users", "customers", "conversations", "messages", "offers", "attributions"):
                conn.execute(
                    text(f"SELECT setval(pg_get_serial_sequence('{table}','id'), (SELECT MAX(id) FROM {table}))")
                )
    except Exception:
        pass


def reset_database():
    with engine.begin() as conn:
        conn.execute(text(
            "TRUNCATE TABLE refresh_tokens, attributions, messages, offers, "
            "conversations, customers, users, companies, "
            "checkpoints, checkpoint_blobs, checkpoint_writes "
            "RESTART IDENTITY CASCADE"
        ))
    print("TRUNCATED all app tables (RESTART IDENTITY CASCADE); ids will restart at 1.")


def print_summary(session):
    counts = [
        ("companies", session.query(Company).count()),
        ("users", session.query(User).count()),
        ("customers", session.query(Customer).count()),
        ("conversations", session.query(Conversation).count()),
        ("messages", session.query(Message).count()),
        ("offers", session.query(Offer).count()),
        ("attributions", session.query(Attribution).count()),
    ]
    print("\nSeed data completed successfully!\n")
    print(f"  {'table':<16} count")
    print(f"  {'-'*24}")
    for table, count in counts:
        print(f"  {table:<16} {count}")
    print(f"\n  Demo logins (shared password: {SEED_PASSWORD}):")
    for user_data in SNAPSHOT_USERS:
        print(f"    {user_data['email']:<25} ({user_data['role']})")


def seed(reset=False):
    if reset:
        reset_database()

    session = SessionLocal()
    try:
        password_hash = hash_password(SEED_PASSWORD)

        for row in SNAPSHOT_COMPANIES:
            _upsert(session, Company, row["id"], {
                "name": row["name"],
                "sector": row["sector"],
                "subscription_tier": row["subscription_tier"],
                "created_at": _dt(row["created_at"]),
            })

        for row in SNAPSHOT_USERS:
            _upsert(session, User, row["id"], {
                "company_id": row["company_id"],
                "full_name": row["full_name"],
                "email": row["email"],
                "password_hash": password_hash,
                "role": row["role"],
                "created_at": _dt(row["created_at"]),
            })

        for row in SNAPSHOT_CUSTOMERS:
            _upsert(session, Customer, row["id"], {
                "company_id": row["company_id"],
                "name": row["name"],
                "phone": row["phone"],
                "password_hash": password_hash,
                "current_plan": row["current_plan"],
                "service_type": row["service_type"],
                "speed": row["speed"],
                "usage_percentage": Decimal(row["usage_percentage"]),
                "contract_end_date": _date(row["contract_end_date"]),
                "segment": row["segment"],
                "interests": row["interests"],
                "location": row["location"],
                "created_at": _dt(row["created_at"]),
            })

        for row in SNAPSHOT_CONVERSATIONS:
            _upsert(session, Conversation, row["id"], {
                "customer_id": row["customer_id"],
                "company_id": row["company_id"],
                "status": row["status"],
                "started_at": _dt(row["started_at"]),
                "closed_at": _dt(row["closed_at"]),
            })

        for row in SNAPSHOT_MESSAGES:
            _upsert(session, Message, row["id"], {
                "conversation_id": row["conversation_id"],
                "sender": row["sender"],
                "text": row["text"],
                "sent_at": _dt(row["sent_at"]),
            })

        for row in SNAPSHOT_OFFERS:
            _upsert(session, Offer, row["id"], {
                "customer_id": row["customer_id"],
                "conversation_id": row["conversation_id"],
                "company_id": row["company_id"],
                "product_name": row["product_name"],
                "price": Decimal(row["price"]),
                "status": row["status"],
                "accepted_at": _dt(row["accepted_at"]),
                "created_at": _dt(row["created_at"]),
            })

        for row in SNAPSHOT_ATTRIBUTIONS:
            _upsert(session, Attribution, row["id"], {
                "conversation_id": row["conversation_id"],
                "customer_id": row["customer_id"],
                "product_id": row["product_id"],
                "product_name": row["product_name"],
                "price": Decimal(row["price"]),
                "status": row["status"],
                "created_at": _dt(row["created_at"]),
                "confirmed_at": _dt(row["confirmed_at"]),
            })

        session.commit()
        _reset_sequences()
        print_summary(session)
    except Exception as e:
        session.rollback()
        print(f"Seeding failed: {e}")
        raise
    finally:
        session.close()


def main():
    parser = ArgumentParser(description="Seed Sellince demo data (exact snapshot).")
    parser.add_argument(
        "--reset",
        action="store_true",
        help="TRUNCATE all app tables (RESTART IDENTITY CASCADE) before seeding.",
    )
    parser.add_argument(
        "--scale",
        choices=["small", "medium", "large"],
        default="medium",
        help="Accepted for backwards compatibility; the full snapshot is always seeded.",
    )
    args = parser.parse_args()
    if args.scale != "medium":
        print(f"NOTE: --scale {args.scale} is accepted for compatibility; seeding full snapshot.")
    seed(reset=args.reset)


if __name__ == "__main__":
    main()
