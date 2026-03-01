from dataclasses import dataclass
from uuid import UUID

from ledger.application.common.queries import Query, QueryHandler
from ledger.application.ledger.dto import LedgerDTO
from ledger.application.ledger.interfaces import LedgerReader
from ledger.application.ledger.exceptions import TransactionNotFoundException


@dataclass(frozen=True)
class GetLedgerByTransactionIDQuery(Query):
    transaction_id: UUID


class GetLedgersByTransactionIDHandler(QueryHandler[LedgerDTO]):
    def __init__(self, reader: LedgerReader) -> None:
        self._reader = reader

    async def __call__(self, query: GetLedgerByTransactionIDQuery) -> LedgerDTO:
        ledger = await self._reader.get_by_transaction_id(query.transaction_id)

        if ledger is None:
            raise TransactionNotFoundException(query.transaction_id)

        return ledger
