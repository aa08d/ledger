from uuid import UUID

from ledger.application.common.exceptions import ApplicationException


class LedgerNotFoundException(ApplicationException):
    def __init__(self, ledger_id: UUID) -> None:
        self._ledger_id = ledger_id

    @property
    def message(self) -> str:
        return f'A Ledger with the "{self._ledger_id}" ID doesn\'t exist'
