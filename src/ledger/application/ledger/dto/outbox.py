from dataclasses import dataclass
from uuid import UUID

from ledger.application.common.dto import DTO


@dataclass(frozen=True)
class OutboxMessageDTO(DTO):
    id: UUID
    event_type: str
    payload: dict
    aggregate_id: UUID | None = None
    aggregate_type: str | None = None
