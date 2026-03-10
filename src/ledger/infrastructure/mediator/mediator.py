from typing import TypeVar

from dishka import AsyncContainer

from ledger.application.common.interfaces import Mediator
from ledger.application.common.commands import Command, CommandHandler
from ledger.application.common.queries import Query, QueryHandler
from ledger.domain.common.events import Event, EventHandler


RR = TypeVar("RR")


class MediatorImpl(Mediator):
    def __init__(self, container: AsyncContainer) -> None:
        super().__init__()
        self._container = container

    async def send(self, request: Command | Query) -> RR:
        handler_type = self._request_handlers.get(type(request))

        if handler_type is None:
            raise ValueError(f"No handler registered for {type(request).__name__}")

        async with self._container() as container:
            handler: CommandHandler | QueryHandler = await container.get(handler_type)
            return await handler(request)

    async def publish(self, events: Event | list[Event]) -> None:
        if isinstance(events, Event):
            events = [events]

        async with self._container() as container:
            for event in events:
                handlers = self._event_handlers.get(type(event), [])
                for handler_type in handlers:
                    handler: EventHandler = await container.get(handler_type)
                    await handler(event)
