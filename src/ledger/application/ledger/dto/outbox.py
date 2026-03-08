from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from ledger.application.common.dto import DTO


@dataclass(frozen=True)
class OutboxMessageDTO(DTO):
    id: UUID
    event: str
    payload: dict
    created_at: datetime
    published_at: datetime | None
