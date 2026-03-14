from abc import ABC, abstractmethod
from uuid import UUID

from ledger.infrastructure.inbox.message import InboxMessage



class Inbox(ABC):
    @abstractmethod
    async def save(self, message: InboxMessage) -> None: ...

    @abstractmethod
    async def next(self, batch_size: int) -> list[InboxMessage]: ...

    @abstractmethod
    async def mark_processed(self, message_ids: list[UUID]) -> None: ...
