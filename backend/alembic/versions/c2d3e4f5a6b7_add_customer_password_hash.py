"""add customer password hash"""

from alembic import op
import sqlalchemy as sa


revision = "c2d3e4f5a6b7"
down_revision = "a1b2c3d4e5f6"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("customers", sa.Column("password_hash", sa.String(length=255), nullable=True))


def downgrade() -> None:
    op.drop_column("customers", "password_hash")