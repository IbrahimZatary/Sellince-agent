from collections import Counter
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.api.auth import get_current_user
from app.core.database import get_db
from app.models.attribution import Attribution
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

WEEKDAYS = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]


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

    completed_attributions = (
        db.query(Attribution)
        .join(Conversation, Attribution.conversation_id == Conversation.id)
        .filter(
            Conversation.company_id == company_id,
            Attribution.status == "completed",
        )
        .all()
    )

    completed_count = len(completed_attributions)

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
            value=f"{_pct(completed_count, offer_count)}%",
        ),
        OverviewMetric(
            id="customers",
            label="Customers Served",
            value=customer_count,
        ),
    ]

    # Start from previous Sunday
    now = datetime.now(timezone.utc).replace(
        tzinfo=None, hour=0, minute=0, second=0, microsecond=0
    )
    days_since_sunday = (now.weekday() + 1) % 7  # Monday=0...Sunday=6 -> Sunday=0
    day_start = now - timedelta(days=days_since_sunday)
    totals = (
        db.query(
            func.date(Attribution.created_at),
            func.coalesce(func.sum(Attribution.price), 0),
        )
        .join(Conversation, Attribution.conversation_id == Conversation.id)
        .filter(
            Conversation.company_id == company_id,
            Attribution.status == "completed",
            Attribution.created_at >= day_start,
        )
        .group_by(func.date(Attribution.created_at))
        .all()
    )
    revenue_by_day = {str(day): float(total) for day, total in totals}
    revenue_trend = [
        TrendPoint(
            date=WEEKDAYS[(day.weekday() + 1) % 7],
            revenue=revenue_by_day.get(str(day.date()), 0.0),
        )
        for day in (day_start + timedelta(days=offset) for offset in range(7))
    ]

    category_revenue: "Counter[str] | dict[str, float]" = Counter()
    for attr in completed_attributions:
        category = _offer_category(attr.product_name)
        category_revenue[category] += float(attr.price)
    total_paid = sum(category_revenue.values()) or 0.0
    # Every category the team actually offered appears — 0 where never paid —
    # so the dashboard is complete (same principle as the funnel, which lists
    # all stages). Add-ons is offered but never paid in the seed → 0, present.
    offered_categories = {_offer_category(o.product_name) for o in offers}
    revenue_by_offer = [
        OfferShare(category=category, value=_pct(round(category_revenue[category], 2), total_paid))
        for category in sorted(offered_categories)
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
        .filter(
            Conversation.company_id == company_id,
            Message.sender.in_(["agent", "ai_agent"]),
        )
        .order_by(Message.sent_at.desc())
        .limit(20)
        .all()
    )
    conversation_ids = {conversation.id for _, conversation, _ in recent}
    latest_offer_by_conversation = {}
    completed_conv_ids = set()
    declined_conv_ids = set()
    sent_conv_ids = set()
    if conversation_ids:
        offers_for_activity = (
            db.query(Offer)
            .filter(Offer.conversation_id.in_(conversation_ids))
            .order_by(Offer.created_at.desc())
            .all()
        )
        for offer in offers_for_activity:
            latest_offer_by_conversation.setdefault(offer.conversation_id, offer)

        # Find conversations with completed attributions
        completed_attributions_conv = (
            db.query(Attribution.conversation_id)
            .filter(
                Attribution.conversation_id.in_(conversation_ids),
                Attribution.status == "completed",
            )
            .distinct()
            .all()
        )
        completed_conv_ids = {c[0] for c in completed_attributions_conv}

        # Find conversations with declined offers
        declined_offers_conv = (
            db.query(Offer.conversation_id)
            .filter(
                Offer.conversation_id.in_(conversation_ids),
                Offer.status == "declined",
            )
            .distinct()
            .all()
        )
        declined_conv_ids = {c[0] for c in declined_offers_conv}

        # Find conversations with sent offers (not declined, not completed)
        sent_offers_conv = (
            db.query(Offer.conversation_id)
            .filter(
                Offer.conversation_id.in_(conversation_ids),
                Offer.status == "sent",
            )
            .distinct()
            .all()
        )
        sent_conv_ids = {c[0] for c in sent_offers_conv}

    def _activity_status(conversation):
        if conversation.id in completed_conv_ids:
            return "confirmed"
        if conversation.id in declined_conv_ids:
            return "declined"
        if conversation.id in sent_conv_ids:
            return "sent"
        if conversation.status == "closed":
            return "handed to human"
        return "in progress"

    recent_activity = [
        ActivityRow(
            id=message.id,
            customer=customer.name,
            identifier=customer.phone,
            signal=customer.service_type or customer.current_plan,
            action=(latest_offer_by_conversation.get(conversation.id).product_name
                    if latest_offer_by_conversation.get(conversation.id)
                    else "No offer"),
            status=_activity_status(conversation),
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
            FunnelStage(stage="Closed", count=completed_count, percentage=_pct(completed_count, conv_count)),
        ],
        revenueByOffer=revenue_by_offer,
        agentAutonomy=agent_autonomy,
        recentActivity=recent_activity,
    )
