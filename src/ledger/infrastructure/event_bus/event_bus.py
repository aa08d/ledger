import orjson
import logging

from aio_pika import Message, DeliveryMode
from aio_pika.abc import AbstractChannel

from ledger.application.ledger.interfaces import EventBus
from ledger.application.ledger.dto import OutboxMessageDTO


logger = logging.getLogger(__name__)


class RabbitMQEventBus(EventBus):
    def __init__(self, channel: AbstractChannel) -> None:
        self._channel = channel

    async def publish(self, events: list[OutboxMessageDTO]) -> None:
        for event in events:
            await self._channel.default_exchange.publish(
                Message(
                    body=orjson.dumps(event.payload),
                    message_id=str(event.id),
                    type=event.event,
                    content_type="application/json",
                    delivery_mode=DeliveryMode.PERSISTENT,
                ),
                routing_key=event.event,
            )
            logger.info(f"Published event={event.event} message_id={event.id}")
