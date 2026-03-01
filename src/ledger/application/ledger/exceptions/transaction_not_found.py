from uuid import UUID

from ledger.application.common.exceptions import ApplicationException


class TransactionNotFoundException(ApplicationException):
    def __init__(self, transaction_id: UUID) -> None:
        self._transaction_id = transaction_id

    @property
    def message(self) -> str:
        return f'A Ledger with the "{self._transaction_id}" Transaction ID doesn\'t exist'
