from sqlalchemy import sql, Table, Column, UUID, String, JSON, DateTime

from ledger.infrastructure.persistence.models import BaseModel


inbox_messages_table = Table(
    "inbox_messages",
    BaseModel.metadata,
    Column("id", UUID(as_uuid=True), primary_key=True),
    Column("event", String(255), nullable=False),
    Column("payload", JSON, nullable=False),
    Column("created_at", DateTime(timezone=True), default=sql.func.now()),
    Column("processed_at", DateTime(timezone=True), nullable=True, default=None),
)
