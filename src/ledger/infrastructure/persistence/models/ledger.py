from sqlalchemy import Table, Column, UUID, Enum, BigInteger, String

from ledger.domain.ledger.value_objects import LedgerType, CurrencyCode, LedgerStatus

from .base import TimedBaseModel


ledgers_table = Table(
    "ledgers",
    TimedBaseModel.metadata,
    Column("id", UUID(as_uuid=True), primary_key=True),
    Column("wallet_id", UUID(as_uuid=True)),
    Column("transaction_id", UUID(as_uuid=True), unique=True),
    Column("type", Enum(LedgerType)),
    Column("amount", BigInteger),
    Column("currency", Enum(CurrencyCode)),
    Column("status", Enum(LedgerStatus)),
    Column("code", String(2)),
    Column("details", String(255)),
)
