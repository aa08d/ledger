from sqlalchemy.ext.asyncio import AsyncSession

from ledger.domain.ledger.repository import LedgerRepository
from ledger.domain.ledger.entities import Ledger
from ledger.domain.ledger.value_objects import LedgerID


class SQLAlchemyLedgerRepository(LedgerRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def acquire_by_id(self, ledger_id: LedgerID) -> Ledger | None:
        ledger = await self._session.get(
            Ledger,
            ledger_id.value,
            with_for_update=True,
        )

        return ledger

    async def save(self, ledger: Ledger) -> None:
        self._session.add(ledger)
