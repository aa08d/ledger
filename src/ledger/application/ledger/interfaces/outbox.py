from abc import ABC, abstractmethod
from uuid import UUID

from ledger.domain.common.events import Event
from ledger.application.ledger.dto import OutboxMessageDTO


class Outbox(ABC):
    @abstractmethod
    async def append(self, events: list[Event]) -> None: ...

    @abstractmethod
    async def next(self, limit: int) -> list[OutboxMessageDTO]: ...

    @abstractmethod
    async def done(self, messages: list[UUID]) -> None: ...
