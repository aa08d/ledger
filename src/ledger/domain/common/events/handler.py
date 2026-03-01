from abc import ABC, abstractmethod

from .event import Event


class EventHandler[ER](ABC):
    @abstractmethod
    async def __call__(self, event: Event) -> ER: ...
