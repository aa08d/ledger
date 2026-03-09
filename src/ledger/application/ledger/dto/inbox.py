from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from ledger.application.common.dto import DTO



@dataclass(frozen=True)
class InboxMessageDTO(DTO):
    message_id: UUID
    event: str
    payload: dict
    created_at: datetime
