import orjson
import logging

from uuid import UUID
from datetime import datetime, UTC

from aio_pika.abc import AbstractIncomingMessage

from ledger.application.common.interfaces import UnitOfWork, Mediator
from ledger.domain.common.events import Event
from ledger.application.ledger.dto import InboxMessageDTO
from ledger.application.ledger.interfaces import Inbox

from .converters import convert_inbox_message_to_integration_event


logger = logging.getLogger(__name__)


class InboxConsumer:
    def __init__(
        self,
        mediator: Mediator,
        inbox: Inbox,
        uow: UnitOfWork,
    ) -> None:
        self._mediator = mediator
        self._inbox = inbox
        self._uow = uow

    async def __call__(self, message: AbstractIncomingMessage) -> None:
        async with message.process(requeue=True, ignore_processed=True):
            try:
                await self._process(message)
            except Exception:
                logger.exception(
                    "Failed to process message, requeueing. "
                    "routing_key=%s message_id=%s",
                    message.routing_key,
                    message.message_id,
                )
                await message.nack(requeue=True)

    async def _process(self, message: AbstractIncomingMessage) -> None:
        inbox_message = InboxMessageDTO(
            message_id=UUID(message.message_id),
            event=message.routing_key,
            payload=orjson.loads(message.body),
            created_at=datetime.now(UTC),
        )

        if await self._inbox.exists(inbox_message.message_id):
            logger.info("Duplicate message_id=%s, skipping", inbox_message.message_id)
            return await message.ack()

        event: Event = convert_inbox_message_to_integration_event(inbox_message)

        await self._inbox.save(inbox_message)
        await self._mediator.publish(event)
        await self._inbox.done(inbox_message.message_id)
        await self._uow.commit()

        logger.info(
            "Processed event=%s message_id=%s",
            inbox_message.event,
            inbox_message.message_id,
        )

        return await message.ack()
