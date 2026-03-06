from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from ledger.application.common.pagination import Pagination, SortOrder, PaginationResult
from ledger.application.ledger.dto import LedgerDTO, LedgersDTO
from ledger.application.ledger.interfaces import LedgerReader, LedgerFilters
from ledger.domain.common.constants import Empty
from ledger.infrastructure.persistence.models import ledgers_table
from ledger.infrastructure.persistence.converters import covert_ledger_row_to_dto



class SQLAlchemyLedgerReader(LedgerReader):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, ledger_id: UUID) -> LedgerDTO | None:
        stmt = await self._session.execute(
            select(ledgers_table).where(ledgers_table.c.id == ledger_id),
        )
        ledger = stmt.mappings().one_or_none()

        if ledger is None:
            return None

        return covert_ledger_row_to_dto(ledger)

    async def get_by_transaction_id(self, transaction_id: UUID) -> LedgerDTO | None:
        stmt = await self._session.execute(
            select(ledgers_table).where(ledgers_table.c.transaction_id == transaction_id),
        )
        ledger = stmt.mappings().one_or_none()

        if ledger is None:
            return None

        return covert_ledger_row_to_dto(ledger)


    async def get_ledgers(self, filters: LedgerFilters, pagination: Pagination) -> LedgersDTO:
        stmt = select(ledgers_table)

        if filters.wallet_id is not Empty.UNSET:
            stmt = stmt.filter(ledgers_table.c.wallet_id == filters.wallet_id)

        if filters.type is not Empty.UNSET:
            stmt = stmt.filter(ledgers_table.c.type == filters.type)

        if filters.status is not Empty.UNSET:
            stmt = stmt.filter(ledgers_table.c.status == filters.status)

        if filters.currency is not Empty.UNSET:
            stmt = stmt.filter(ledgers_table.c.currency == filters.currency)

        ledgers_count: int = await self._session.scalar(
            select(func.count()).select_from(stmt.subquery())
        )

        if pagination.order is SortOrder.ASC:
            stmt = stmt.order_by(ledgers_table.c.id.asc())

        if pagination.order is SortOrder.DESC:
            stmt = stmt.order_by(ledgers_table.c.id.desc())

        if pagination.offset is not Empty.UNSET:
            stmt = stmt.offset(pagination.offset)

        if pagination.limit is not Empty.UNSET:
            stmt = stmt.limit(pagination.limit)

        ledgers_rows = await self._session.execute(stmt)
        ledgers = [covert_ledger_row_to_dto(ledger) for ledger in ledgers_rows.scalars()]

        return LedgersDTO(
            data=ledgers,
            pagination=PaginationResult.from_pagination(
                pagination=pagination,
                total=ledgers_count,
            ),
        )
