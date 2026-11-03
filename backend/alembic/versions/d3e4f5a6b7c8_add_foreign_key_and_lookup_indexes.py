"""add foreign key and lookup indexes

Revision ID: d3e4f5a6b7c8
Revises: 9e0eefc0c69e
Create Date: 2026-11-03 18:20:00.000000

"""
from alembic import op


revision = 'd3e4f5a6b7c8'
down_revision = '9e0eefc0c69e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_index(op.f('ix_messages_conversation_id'), 'messages', ['conversation_id'], unique=False)
    op.create_index(op.f('ix_conversations_customer_id'), 'conversations', ['customer_id'], unique=False)
    op.create_index(op.f('ix_conversations_company_id'), 'conversations', ['company_id'], unique=False)
    op.create_index(op.f('ix_customers_company_id'), 'customers', ['company_id'], unique=False)
    op.create_index(op.f('ix_customers_phone'), 'customers', ['phone'], unique=False)
    op.create_index(op.f('ix_attributions_conversation_id'), 'attributions', ['conversation_id'], unique=False)
    op.create_index(op.f('ix_attributions_customer_id'), 'attributions', ['customer_id'], unique=False)
    op.create_index(op.f('ix_offers_conversation_id'), 'offers', ['conversation_id'], unique=False)
    op.create_index(op.f('ix_offers_customer_id'), 'offers', ['customer_id'], unique=False)
    op.create_index(op.f('ix_offers_company_id'), 'offers', ['company_id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_offers_company_id'), table_name='offers')
    op.drop_index(op.f('ix_offers_customer_id'), table_name='offers')
    op.drop_index(op.f('ix_offers_conversation_id'), table_name='offers')
    op.drop_index(op.f('ix_attributions_customer_id'), table_name='attributions')
    op.drop_index(op.f('ix_attributions_conversation_id'), table_name='attributions')
    op.drop_index(op.f('ix_customers_phone'), table_name='customers')
    op.drop_index(op.f('ix_customers_company_id'), table_name='customers')
    op.drop_index(op.f('ix_conversations_company_id'), table_name='conversations')
    op.drop_index(op.f('ix_conversations_customer_id'), table_name='conversations')
    op.drop_index(op.f('ix_messages_conversation_id'), table_name='messages')
