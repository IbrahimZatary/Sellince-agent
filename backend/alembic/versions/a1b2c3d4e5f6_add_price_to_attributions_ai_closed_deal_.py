"""add price to attributions

Revision ID: a1b2c3d4e5f6
Revises: ec75bd3d3ac8
Create Date: 2026-09-21 00:15:00.000000

"""
from alembic import op
import sqlalchemy as sa

revision = 'a1b2c3d4e5f6'
down_revision = 'ec75bd3d3ac8'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Give attributions the price column the app has always expected.

    The model, schemas and router already snapshot price at POST time
    (single source of truth for revenue — there is no products table to
    re-fetch from). The migration that created the table just never added
    the column, so live Postgres rejects every insert. Add it now,
    freezing the agreed amount exactly like the model already does.
    """
    op.add_column(
        'attributions',
        sa.Column('price', sa.Numeric(10, 2), nullable=False, server_default='0'),
    )


def downgrade() -> None:
    op.drop_column('attributions', 'price')
