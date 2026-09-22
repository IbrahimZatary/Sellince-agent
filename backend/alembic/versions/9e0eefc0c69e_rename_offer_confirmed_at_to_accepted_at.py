"""rename offer.confirmed_at to accepted_at

Revision ID: 9e0eefc0c69e
Revises: bfad3099a3fc
Create Date: 2026-09-22 06:53:47.738239

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9e0eefc0c69e'
down_revision = 'bfad3099a3fc'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column('offers', 'confirmed_at', new_column_name='accepted_at')


def downgrade() -> None:
    op.alter_column('offers', 'accepted_at', new_column_name='confirmed_at')