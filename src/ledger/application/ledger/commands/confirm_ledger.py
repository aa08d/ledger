from dataclasses import dataclass
from uuid import UUID

from ledger.application.common.commands import Command


@dataclass(frozen=True)
class ConfirmLedgerCommand(Command):
    ledger_id: UUID
    code: str
    details: str
