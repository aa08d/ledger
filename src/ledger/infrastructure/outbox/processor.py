import asyncio
import logging

from ledger.application.common.interfaces import UnitOfWork

from .interfaces import Outbox, OutboxPublisher
from .config import OutboxConfig


logger = logging.getLogger(__name__)


class OutboxProcessor:
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
        self._current_task: asyncio.Task | None = None

    async def start(self) -> None:
        self._current_task = asyncio.current_task()
        logger.info(
            "OutboxProcessor started",
            extra={
                "poll_interval": self._config.poll_interval,
                "batch_size": self._config.batch_size,
            },
        )

        loop = asyncio.get_running_loop()

        while not self._stop_event.is_set():
            start_time = loop.time()
            await self._process_batch()
            elapsed = loop.time() - start_time
            await asyncio.sleep(max(0.0, self._config.poll_interval - elapsed))

    async def stop(self) -> None:
        self._stop_event.set()
        if self._current_task:
            await self._current_task

        logger.info("OutboxProcessor stopped")

    async def _process_batch(self) -> None:
        messages = await self._outbox.next(self._config.batch_size)

        if not messages:
            return

        await self._publisher.publish(messages)
        await self._outbox.mark_processed([m.id for m in messages])
        await self._uow.commit()

        logger.info("OutboxPoller published %d messages", len(messages))
