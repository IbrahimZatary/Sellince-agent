from collections import Counter
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.api.auth import get_current_user
from app.core.database import get_db
from app.models.conversation import Conversation
from app.models.customer import Customer
from app.models.message import Message
from app.models.offer import Offer
from app.models.user import User
from app.schemas.dashboard import (
    ActivityRow,
    AutonomySlice,
    DashboardSummary,
    FunnelStage,
    OfferShare,
    OverviewMetric,
    TrendPoint,
)

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

WEEKDAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


def _offer_category(product_name: str) -> str:
    name = (product_name or "").lower()
    if "add" in name and "on" in name:
        return "Add-ons"
    if "fiber" in name:
        return "Broadband"
    return "Data Upgrades"


def _relative_time(ts: datetime) -> str:
    delta = datetime.now(timezone.utc).replace(tzinfo=None) - ts.replace(tzinfo=None)
    seconds = int(delta.total_seconds())
    if seconds < 60:
        return "just now"
    if seconds < 3600:
        return f"{seconds // 60} min ago"
    if seconds < 86400:
        return f"{seconds // 3600} hrs ago"
    return f"{seconds // 86400} days ago"


def _pct(part: int, total: int) -> int:
    return round(part / total * 100) if total else 0


@router.get("/summary", response_model=DashboardSummary)
def dashboard_summary(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    company_id = current_user.company_id

    conversations = (
        db.query(Conversation)
        .filter(Conversation.company_id == company_id)
        .all()
    )
    conv_count = len(conversations)
    open_count = sum(1 for c in conversations if c.status == "open")
    closed_count = sum(1 for c in conversations if c.status == "closed")

    offers = db.query(Offer).filter(Offer.company_id == company_id).all()
    offer_count = len(offers)
    accepted_count = sum(1 for o in offers if o.status == "accepted")

    customer_count = (
        db.query(Customer).filter(Customer.company_id == company_id).count()
    )

    replied_count = (
        db.query(Message.conversation_id)
        .join(Conversation, Message.conversation_id == Conversation.id)
        .filter(Conversation.company_id == company_id)
        .group_by(Message.conversation_id)
        .having(func.count(Message.id) >= 2)
        .count()
    )

    overview_metrics = [
        OverviewMetric(
            id="conversations",
            label="Conversations Handled",
            value=conv_count,
        ),
        OverviewMetric(
            id="offers",
            label="Offers Presented",
            value=offer_count,
        ),
        OverviewMetric(
            id="conversion",
            label="Conversion Rate",
            value=f"{_pct(accepted_count, offer_count)}%",
        ),
        OverviewMetric(
            id="customers",
            label="Customers Served",
            value=customer_count,
        ),
    ]

    day_start = datetime.now(timezone.utc).replace(
        tzinfo=None, hour=0, minute=0, second=0, microsecond=0
    ) - timedelta(days=6)
    totals = (
        db.query(
            func.date(Offer.created_at),
            func.coalesce(func.sum(Offer.price), 0),
        )
        .filter(Offer.company_id == company_id, Offer.created_at >= day_start)
        .group_by(func.date(Offer.created_at))
        .all()
    )
    revenue_by_day = {str(day): float(total) for day, total in totals}
    revenue_trend = [
        TrendPoint(
            date=WEEKDAYS[day.weekday()],
            revenue=revenue_by_day.get(str(day.date()), 0.0),
        )
        for day in (day_start + timedelta(days=offset) for offset in range(7))
    ]

    category_totals = Counter(
        _offer_category(o.product_name) for o in offers
    )
    total_offers = sum(category_totals.values())
    revenue_by_offer = [
        OfferShare(category=category, value=_pct(count, total_offers))
        for category, count in category_totals.items()
    ]

    agent_autonomy = [
        AutonomySlice(status="Auto-resolved", percentage=_pct(closed_count, conv_count)),
        AutonomySlice(status="Handed to human", percentage=0),
        AutonomySlice(status="Follow-up queued", percentage=_pct(open_count, conv_count)),
    ]

    recent = (
        db.query(Message, Conversation, Customer)
        .join(Conversation, Message.conversation_id == Conversation.id)
        .join(Customer, Conversation.customer_id == Customer.id)
        .filter(Conversation.company_id == company_id)
        .order_by(Message.sent_at.desc())
        .limit(10)
        .all()
    )
    recent_activity = [
        ActivityRow(
            id=message.id,
            customer=customer.name,
            identifier=customer.phone,
            signal=customer.service_type or customer.current_plan,
            action=(
                message.text[:60] + "…" if len(message.text) > 60 else message.text
            ),
            status=conversation.status,
            timestamp=_relative_time(message.sent_at),
        )
        for message, conversation, customer in recent
    ]

    return DashboardSummary(
        overviewMetrics=overview_metrics,
        revenueTrend=revenue_trend,
        conversionFunnel=[
            FunnelStage(stage="Engaged", count=conv_count, percentage=100),
            FunnelStage(stage="Replied", count=replied_count, percentage=_pct(replied_count, conv_count)),
            FunnelStage(stage="Offer Presented", count=offer_count, percentage=_pct(offer_count, conv_count)),
            FunnelStage(stage="Closed", count=closed_count, percentage=_pct(closed_count, conv_count)),
        ],
        revenueByOffer=revenue_by_offer,
        agentAutonomy=agent_autonomy,
        recentActivity=recent_activity,
    )