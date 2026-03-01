from abc import ABC, abstractmethod

from ledger.domain.ledger.value_objects import LedgerID
from ledger.domain.ledger.entities import Ledger


class LedgerRepository(ABC):
    @abstractmethod
    async def acquire_by_id(self, ledger_id: LedgerID) -> Ledger | None:
        raise NotImplementedError

    @abstractmethod
    async def save(self, ledger: Ledger) -> Ledger | None:
        raise NotImplementedError
