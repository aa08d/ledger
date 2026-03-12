from abc import ABC, abstractmethod

from ledger.infrastructure.outbox.message import OutboxMessage


class OutboxPublisher(ABC):
    @abstractmethod
    async def publish(self, messages: list[OutboxMessage]) -> None: ...
