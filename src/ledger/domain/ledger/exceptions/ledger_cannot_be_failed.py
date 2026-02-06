from uuid import UUID

from ledger.domain.common.exceptions import DomainException


class LedgerCannotBeFailed(DomainException):
    def __init__(self, ledger_id: UUID, status: str) -> None:
        self._ledger_id = ledger_id
        self._status = status

    @property
    def message(self) -> str:
        return f"Ledger {self._ledger_id} cannot be failed from status '{self._status}'"
