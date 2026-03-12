import orjson

from dataclasses import asdict

from ledger.domain.common.events import Event, EventHandler

from .interfaces import Outbox
from .message import OutboxMessage


class OutboxEventHandler(EventHandler):
    def __init__(self, outbox: Outbox) -> None:
        self._outbox = outbox

    async def __call__(self, event: Event) -> None:
        message = OutboxMessage(
            id=event.event_id,
            event= type(event).__name__,
            payload=orjson.loads(orjson.dumps(asdict(event))),
            created_at=event.event_timestamp,
        )
        await self._outbox.append(message)
