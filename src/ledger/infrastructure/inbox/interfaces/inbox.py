from abc import ABC, abstractmethod
from uuid import UUID

from ledger.infrastructure.inbox.message import InboxMessage



class Inbox(ABC):
    @abstractmethod
    async def exists(self, message_id: UUID) -> bool: ...

    @abstractmethod
    async def save(self, message: InboxMessage) -> None: ...

    @abstractmethod
    async def done(self, message_id: UUID) -> None: ...
