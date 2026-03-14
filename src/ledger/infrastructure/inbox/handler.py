import logging
import orjson
import re

from dataclasses import asdict

from ledger.application.common.interfaces import UnitOfWork
from ledger.domain.common.events import Event

from .message import InboxMessage
from .interfaces import Inbox


logger = logging.getLogger(__name__)


class InboxEventHandler:
    def __init__(self, inbox: Inbox, uow: UnitOfWork) -> None:
        self._inbox = inbox
        self._uow = uow

    async def __call__(self, event: Event) -> None:
        routing_key = re.sub(r"(?<!^)(?=[A-Z])", ".", type(event).__name__).lower()
        message = InboxMessage(
            id=event.event_id,
            event=routing_key,
            payload=orjson.loads(orjson.dumps(asdict(event))),
            created_at=event.event_timestamp,
        )
        await self._inbox.save(message)
        await self._uow.commit()

        logger.info("Processed event=%s message_id=%s", message.event, message.id)
