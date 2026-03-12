import asyncio
import logging

from ledger.application.common.interfaces import UnitOfWork

from .interfaces import Outbox, OutboxPublisher
from .config import OutboxConfig


logger = logging.getLogger(__name__)


class OutboxPoller:
    def __init__(
        self,
        config: OutboxConfig,
        outbox: Outbox,
        publisher: OutboxPublisher,
        uow: UnitOfWork,
    ) -> None:
        self._config = config
        self._outbox = outbox
        self._publisher = publisher
        self._uow = uow

        self._stop_event = asyncio.Event()

    async def start(self) -> None:
        while not self._stop_event.is_set():
            pass


    async def stop(self) -> None:
        self._stop_event.set()

    async def _process_batch(self) -> None:
        messages = await self._outbox.next(self._config.batch_size)

        if not messages:
            await asyncio.sleep(self._config.poll_interval)
            return

        await self._publisher.publish(messages)
        await self._outbox.done([m.id for m in messages])
        await self._uow.commit()

        logger.info("Outbox poller published %d messages", len(messages))
