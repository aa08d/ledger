from abc import ABC, abstractmethod
from typing import Type, TypeVar

from ledger.domain.common.events import Event, EventHandler
from ledger.application.common.commands import Command, CommandHandler
from ledger.application.common.queries import Query, QueryHandler


RR = TypeVar("RR")
Request = Command | Query
RequestHandler = CommandHandler | QueryHandler


class Meditor(ABC):
    def __init__(self) -> None:
        self._request_handlers = {}
        self._event_handlers = {}

    def register(
        self,
        message: Type[Request | Event],
        handler: RequestHandler | EventHandler,
    ) -> None:
        if issubclass(message, Request):
            self._request_handlers[message] = handler
        elif issubclass(message, Event):
            self._event_handlers.setdefault(message, []).append(handler)

    @abstractmethod
    async def send(self, request: Request) -> RR:
        raise NotImplementedError

    @abstractmethod
    async def publish(self, events: Event | list[Event]) -> None:
        raise NotImplementedError
