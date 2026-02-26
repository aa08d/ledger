from abc import ABC, abstractmethod
from uuid import UUID

from ledger.domain.common.events import Event
from ledger.application.ledger.dto import OutboxMessageDTO


class Outbox(ABC):
    @abstractmethod
    async def append(self, events: list[Event]) -> None:
        raise NotImplementedError

    @abstractmethod
    async def next(self, limit: int) -> list[OutboxMessageDTO]:
        raise NotImplementedError

    @abstractmethod
    async def done(self, messages: list[UUID]) -> None:
        raise NotImplementedError
