from abc import ABC, abstractmethod
from dataclasses import dataclass
from uuid import UUID

from ledger.domain.common.constants import Empty
from ledger.domain.ledger.value_objects import LedgerType, LedgerStatus, CurrencyCode
from ledger.application.common.pagination import Pagination
from ledger.application.ledger.dto import LedgerDTO, LedgersDTO


@dataclass(frozen=True)
class LedgerFilters:
    wallet_id: UUID | Empty = Empty.UNSET
    type: LedgerType | Empty = Empty.UNSET
    status: LedgerStatus | Empty = Empty.UNSET
    currency: CurrencyCode | Empty = Empty.UNSET


class LedgerReader(ABC):
    @abstractmethod
    async def get_by_id(self, ledger_id: UUID) -> LedgerDTO | None: ...

    @abstractmethod
    async def get_by_transaction_id(self, transaction_id: UUID) -> LedgerDTO | None: ...

    @abstractmethod
    async def get_ledgers(
        self,
        filters: LedgerFilters,
        pagination: Pagination
    ) -> LedgersDTO: ...
