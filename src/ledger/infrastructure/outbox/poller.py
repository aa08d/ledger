import asyncio
import logging

from ledger.application.common.interfaces import UnitOfWork
from ledger.application.ledger.interfaces import Outbox, EventBus


logger = logging.getLogger(__name__)


RELAY_BATCH_SIZE = 100
RELAY_POLL_INTERVAL = 1.0


class OutboxPoller:
    def __init__(
        self,
        outbox: Outbox,
        event_bus: EventBus,
        uow: UnitOfWork,
    ) -> None:
        self._outbox = outbox
        self._event_bus = event_bus
        self._uow = uow
        self._running = False

    async def start(self) -> None:
        self._running = True

        while self._running:
            try:
                await self._process_batch()
            except Exception:
                await asyncio.sleep(RELAY_POLL_INTERVAL)

    async def stop(self) -> None:
        self._running = False

    async def _process_batch(self) -> None:
        messages = await self._outbox.next(RELAY_BATCH_SIZE)

        if not messages:
            await asyncio.sleep(RELAY_POLL_INTERVAL)
            return

        await self._event_bus.publish(messages)
        await self._outbox.done([m.id for m in messages])
        await self._uow.commit()

        logger.info("Outbox poller published %d messages", len(messages))
