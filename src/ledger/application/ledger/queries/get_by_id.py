from dataclasses import dataclass
from uuid import UUID

from ledger.application.common.queries import Query, QueryHandler
from ledger.application.ledger.dto import LedgerDTO
from ledger.application.ledger.interfaces import LedgerReader
from ledger.application.ledger.exceptions import LedgerNotFoundException


@dataclass(frozen=True)
class GetLedgerByIDQuery(Query):
    ledger_id: UUID


class GetLedgersByIDHandler(QueryHandler[LedgerDTO]):
    def __init__(self, reader: LedgerReader) -> None:
        self._reader = reader

    async def __call__(self, query: GetLedgerByIDQuery) -> LedgerDTO:
        ledger = await self._reader.get_by_id(query.ledger_id)

        if ledger is None:
            raise LedgerNotFoundException(query.ledger_id)

        return ledger
