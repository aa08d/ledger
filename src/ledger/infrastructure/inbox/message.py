from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True)
class InboxMessage:
    id: UUID
    event: str
    payload: dict
    created_at: datetime
    processed_at: datetime | None = None
