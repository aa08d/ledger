from dataclasses import dataclass

from ledger.application.common.pagination import Pagination
from ledger.application.common.queries import Query, QueryHandler
from ledger.application.ledger.dto import LedgersDTO
from ledger.application.ledger.interfaces import LedgerReader, LedgerFilters


@dataclass(frozen=True)
class GetLedgersQuery(Query):
    filters: LedgerFilters
    pagination: Pagination


class GetLedgersHandler(QueryHandler[LedgersDTO]):
    def __init__(self, reader: LedgerReader) -> None:
        self._reader = reader

    async def __call__(self, query: GetLedgersQuery) -> LedgersDTO:
        ledgers = await self._reader.get_ledgers(query.filters, query.pagination)
        return ledgers
