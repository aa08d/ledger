from dataclasses import dataclass
from uuid import UUID

from ledger.application.common.commands import Command


@dataclass(frozen=True)
class CreateLedgerCommand(Command):
    wallet_id: UUID
    transaction_id: UUID
    type: str
    amount: int
    currency: str
    reason: str
