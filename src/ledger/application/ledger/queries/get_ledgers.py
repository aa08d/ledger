import logging

from dataclasses import dataclass

from ledger.application.common.pagination import Pagination
from ledger.application.common.queries import Query, QueryHandler
from ledger.application.ledger.dto import LedgersDTO
from ledger.application.ledger.interfaces import LedgerReader, LedgerFilters


logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class GetLedgersQuery(Query):
    filters: LedgerFilters
    pagination: Pagination


class GetLedgersHandler(QueryHandler[LedgersDTO]):
    def __init__(self, reader: LedgerReader) -> None:
        self._reader = reader

    async def __call__(self, query: GetLedgersQuery) -> LedgersDTO:
        ledgers = await self._reader.get_ledgers(query.filters, query.pagination)
        logger.debug("Get ledgers", extra={
            "ledgers": ledgers,
            "pagination": query.pagination,
            "filters": query.filters,
        })
        return ledgers
