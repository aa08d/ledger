from dataclasses import dataclass
from datetime import datetime
from typing import Any
from uuid import UUID

from ledger.application.common.dto import DTO


@dataclass(frozen=True)
class OutboxMessage(DTO):
    id: UUID
    event: str
    payload: dict[str, Any]
    created_at: datetime
    published_at: datetime | None = None
