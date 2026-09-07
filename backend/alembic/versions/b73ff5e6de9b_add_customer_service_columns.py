"""add customer internet-use-case columns

Revision ID: b73ff5e6de9b
Revises: 1a259f0bce15
Create Date: 2026-09-07

Adds the columns every customer needs for the internet use case
(Mock Customer Data PDF): service_type, speed, interests, location.

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b73ff5e6de9b'
down_revision = '1a259f0bce15'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('customers', sa.Column('service_type', sa.String(length=30), nullable=True))
    op.add_column('customers', sa.Column('speed', sa.String(length=30), nullable=True))
    op.add_column('customers', sa.Column('interests', sa.String(length=255), nullable=True))
    op.add_column('customers', sa.Column('location', sa.String(length=120), nullable=True))


def downgrade() -> None:
    op.drop_column('customers', 'location')
    op.drop_column('customers', 'interests')
    op.drop_column('customers', 'speed')
    op.drop_column('customers', 'service_type')