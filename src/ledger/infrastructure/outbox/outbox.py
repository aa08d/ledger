from datetime import datetime, UTC
from uuid import UUID
from dataclasses import asdict

from sqlalchemy import select, update, insert
from sqlalchemy.ext.asyncio import AsyncSession

from .table import outbox_messages_table
from .message import OutboxMessage
from .interfaces import Outbox


class SQLAlchemyOutbox(Outbox):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def append(self, message: OutboxMessage) -> None:
        await self._session.execute(
            insert(outbox_messages_table).values(asdict(message))
        )

    async def next(self, limit: int) -> list[OutboxMessage]:
        stmt = (
            select(outbox_messages_table)
            .where(outbox_messages_table.c.published_at.is_(None))
            .order_by(outbox_messages_table.c.created_at.asc())
            .limit(limit)
            .with_for_update(skip_locked=True)
        )
        result = await self._session.execute(stmt)
        rows = result.mappings().all()

        return [OutboxMessage(**row) for row in rows]

    async def mark_processed(self, messages: list[UUID]) -> None:
        if not messages:
            return

        await self._session.execute(
            update(outbox_messages_table)
            .where(outbox_messages_table.c.id.in_(messages))
            .values(published_at=datetime.now(UTC))
        )
