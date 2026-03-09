from abc import ABC, abstractmethod

from ledger.application.ledger.dto import OutboxMessageDTO


class EventBus(ABC):
    @abstractmethod
    async def publish(self, events: list[OutboxMessageDTO]) -> None: ...
