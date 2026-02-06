from uuid import UUID

from ledger.domain.common.exceptions import DomainException


class LedgerAlreadyFailed(DomainException):
    def __init__(self, ledger_id: UUID) -> None:
        self._ledger_id = ledger_id

    @property
    def message(self) -> str:
        return f"The Ledger {self._ledger_id} has already been FAILED."
