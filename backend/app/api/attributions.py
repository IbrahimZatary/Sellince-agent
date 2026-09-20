"""POST /api/v1/attributions  — record a sale our AI agent just closed.

The AI agent (recommend/respond team) decides a deal is done and calls this
to (1) persist the attribution and (2) later hand back a checkout link.

Status lifecycle (pending → completed | expired):
    pending:   checkout URL handed to the customer, not yet paid
    completed: customer actually paid → counts toward "deals our AI closed"
    expired:   checkout URL never used / customer abandoned

Marketing/dashboards ask:  SELECT COUNT(*) WHERE status='completed'.
"""

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.api.auth import get_current_user
from app.core.database import get_db
from app.models.attribution import Attribution
from app.models.conversation import Conversation
from app.models.user import User
from app.schemas.attributions import (
    AttributionCreate,
    AttributionRead,
    AttributionUpdate,
)

router = APIRouter(prefix="/attributions", tags=["attributions"])


def _attribution_read(row: Attribution) -> AttributionRead:
    return AttributionRead(
        id=row.id,
        conversation_id=row.conversation_id,
        customer_id=row.customer_id,
        product_id=row.product_id,
        product_name=row.product_name,
        status=row.status,
        created_at=row.created_at,
        updated_at=row.updated_at,
    )


@router.post("", response_model=AttributionRead, status_code=201)
def create_attribution(
    payload: AttributionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Record that the agent closed a deal (status pending; checkout pending)."""

    conversation_company = (
        db.query(Conversation.company_id)
        .filter(Conversation.id == payload.conversation_id)
        .scalar()
    )
    if conversation_company is None:
        raise HTTPException(
            status_code=404,
            detail=f"conversation {payload.conversation_id} not found",
        )
    if conversation_company != current_user.company_id:
        raise HTTPException(
            status_code=403,
            detail="conversation does not belong to your company",
        )

    row = Attribution(
        conversation_id=payload.conversation_id,
        customer_id=payload.customer_id,
        product_id=payload.product_id,
        product_name=payload.product_name,
        status="pending",
    )
    db.add(row)
    db.commit()
    db.refresh(row)

    return _attribution_read(row)


@router.patch("/{attribution_id}", response_model=AttributionRead)
def update_attribution(
    attribution_id: int,
    payload: AttributionUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Move pending → completed (paid) or expired (never used)."""

    row = (
        db.query(Attribution)
        .join(Conversation, Attribution.conversation_id == Conversation.id)
        .filter(
            Attribution.id == attribution_id,
            Conversation.company_id == current_user.company_id,
        )
        .first()
    )
    if row is None:
        raise HTTPException(
            status_code=404,
            detail=f"attribution {attribution_id} not found",
        )

    if row.status == "pending" and payload.status in ("completed", "expired"):
        row.status = payload.status
        row.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(row)
    elif row.status != "pending":
        # idempotent: already moved → just return the stored state unchanged
        pass

    return _attribution_read(row)


@router.get("", response_model=list[AttributionRead])
def list_attributions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """All the agent's closed deals for this company (for the dashboard)."""

    rows = (
        db.query(Attribution)
        .join(Conversation, Attribution.conversation_id == Conversation.id)
        .filter(Conversation.company_id == current_user.company_id)
        .order_by(Attribution.created_at.desc())
        .all()
    )
    return [_attribution_read(row) for row in rows]
