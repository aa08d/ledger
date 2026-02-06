from dataclasses import dataclass
from uuid import UUID

from ledger.domain.common.events import Event


@dataclass(frozen=True)
class LedgerFailed(Event):
    ledger_id: UUID
    wallet_id: UUID
    transaction_id: UUID
    type: str
    amount: int
    currency: str
    status: str
    reason: str
