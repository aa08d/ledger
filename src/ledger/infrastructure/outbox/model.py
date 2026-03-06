from sqlalchemy import Table, Column, UUID, String, JSON, DateTime

from ledger.infrastructure.persistence.models import BaseModel


outbox_messages_table = Table(
    'outbox_messages',
    BaseModel.metadata,
    Column("id", UUID(as_uuid=True), primary_key=True),
    Column("event_type", String(255)),
    Column("payload", JSON),
    Column('aggregate_id', UUID(as_uuid=True), nullable=True),
    Column("aggregate_type", String(255), nullable=True),
    Column("created_at", DateTime(timezone=True)),
    Column("published_at", DateTime(timezone=True), nullable=True),
)
