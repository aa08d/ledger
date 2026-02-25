from uuid import UUID

from ledger.domain.common.exceptions import DomainException


class LedgerCannotTransition(DomainException):
    def __init__(self, ledger_id: UUID, from_status: str, to_status: str) -> None:
        self._ledger_id = ledger_id
        self._from = from_status
        self._to = to_status

    @property
    def message(self) -> str:
        return f"Ledger {self._ledger_id} cannot transition from {self._from} to {self._to}."
