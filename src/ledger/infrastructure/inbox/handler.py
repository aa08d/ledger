import logging

from ledger.application.common.interfaces import UnitOfWork, Mediator

from .message import InboxMessage
from .interfaces import Inbox
from .converters import convert_inbox_message_to_integration_event


logger = logging.getLogger(__name__)


class InboxEventHandler:
    def __init__(
        self,
        mediator: Mediator,
        inbox: Inbox,
        uow: UnitOfWork,
    ) -> None:
        self._mediator = mediator
        self._inbox = inbox
        self._uow = uow

    async def __call__(self, message: InboxMessage) -> None:
        if await self._inbox.exists(message.id):
            return

        event = convert_inbox_message_to_integration_event(message)

        await self._inbox.save(message)
        await self._mediator.publish(event)
        await self._inbox.done(message.id)
        await self._uow.commit()

        logger.info("Processed event=%s message_id=%s", message.event, message.id)
