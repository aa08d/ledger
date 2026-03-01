from dataclasses import dataclass
from uuid import UUID

from ledger.application.common.dto import DTO
from ledger.application.common.pagination import PaginatedItemsDTO
from ledger.domain.ledger.value_objects import LedgerType, LedgerStatus, CurrencyCode


@dataclass(frozen=True)
class LedgerDTO(DTO):
    id: UUID
    wallet_id: UUID
    transaction_id: UUID
    type: LedgerType
    amount: int
    currency: CurrencyCode
    status: LedgerStatus
    code: int
    details: str


LedgersDTO = PaginatedItemsDTO[LedgerDTO]
