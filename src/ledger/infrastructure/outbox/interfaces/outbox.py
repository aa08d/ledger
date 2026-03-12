from abc import ABC, abstractmethod
from uuid import UUID

from ledger.infrastructure.outbox.message import OutboxMessage


class Outbox(ABC):
    @abstractmethod
    async def append(self, message: OutboxMessage) -> None: ...

    @abstractmethod
    async def next(self, limit: int) -> list[OutboxMessage]: ...

    @abstractmethod
    async def done(self, messages: list[UUID]) -> None: ...
