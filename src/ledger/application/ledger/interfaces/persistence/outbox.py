from abc import ABC, abstractmethod
from uuid import UUID

from ledger.application.ledger.dto import OutboxMessageDTO


class Outbox(ABC):
    @abstractmethod
    async def append(self,
        event_type: str,
        payload: dict,
        aggregate_id: UUID | None = None,
        aggregate_type: str | None = None,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def next(self, limit: int) -> list[OutboxMessageDTO]:
        raise NotImplementedError

    @abstractmethod
    async def done(self, messages: list[UUID]) -> None:
        raise NotImplementedError
