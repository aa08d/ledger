import orjson

from datetime import datetime, UTC
from dataclasses import asdict
from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from ledger.application.ledger.dto import OutboxMessageDTO
from ledger.application.ledger.interfaces import Outbox
from ledger.domain.common.events import Event

from .model import outbox_messages_table


class SQLAlchemyOutbox(Outbox):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def append(self, events: list[Event]) -> None:
        if not events:
            return

        rows = [
            {"event": type(e).__name__, "payload": orjson.loads(orjson.dumps(asdict(e)))}
            for e in events
        ]

        await self._session.execute(outbox_messages_table.insert(), rows)

    async def next(self, limit: int) -> list[OutboxMessageDTO]:
        stmt = (
            select(outbox_messages_table)
            .where(outbox_messages_table.c.published_at.is_(None))
            .order_by(outbox_messages_table.c.created_at.asc())
            .limit(limit)
            .with_for_update(skip_locked=True)
        )
        result = await self._session.execute(stmt)
        rows = result.mappings().all()

        return [OutboxMessageDTO(**row) for row in rows]

    async def done(self, messages: list[UUID]) -> None:
        if not messages:
            return

        await self._session.execute(
            update(outbox_messages_table)
            .where(outbox_messages_table.c.id.in_(messages))
            .values(published_at=datetime.now(UTC))
        )
