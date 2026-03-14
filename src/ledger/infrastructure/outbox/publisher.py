import orjson
import logging

from aio_pika import DeliveryMode, Message
from aio_pika.abc import AbstractChannel

from .interfaces import OutboxPublisher
from .message import OutboxMessage


logger = logging.getLogger(__name__)


class RabbitMQOutboxPublisher(OutboxPublisher):
    def __init__(self, channel: AbstractChannel) -> None:
        self._channel = channel

    async def publish(self, messages: list[OutboxMessage]):
        for message in messages:
            await self._channel.default_exchange.publish(
                Message(
                    body=orjson.dumps(message.payload),
                    message_id=str(message.id),
                    type=message.event,
                    content_type="application/json",
                    delivery_mode=DeliveryMode.PERSISTENT,
                ),
                routing_key=message.event,
            )
            logger.info(f"Published event={message.event} message_id={message.id}")
