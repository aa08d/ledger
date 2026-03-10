from abc import ABC, abstractmethod
from uuid import UUID

from ledger.application.ledger.dto import InboxMessageDTO


class Inbox(ABC):
    @abstractmethod
    async def save(self, message: InboxMessageDTO) -> None: ...

    @abstractmethod
    async def done(self, message_id: UUID) -> None: ...
