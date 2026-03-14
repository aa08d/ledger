from datetime import datetime, UTC
from dataclasses import asdict
from uuid import UUID

from sqlalchemy import select, insert, update
from sqlalchemy.ext.asyncio import AsyncSession

from .model import inbox_messages_table
from .interfaces import Inbox
from .message import InboxMessage


class SQLAlchemyInbox(Inbox):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save(self, message: InboxMessage) -> None:
        if await self._exists(message.id):
            return

        await self._session.execute(
            insert(inbox_messages_table)
            .values(asdict(message))
        )

    async def next(self, limit: int) -> list[InboxMessage]:
        stmt = (
            select(inbox_messages_table)
            .where(inbox_messages_table.c.processed_at.is_(None))
            .order_by(inbox_messages_table.c.created_at.asc())
            .limit(limit)
        )
        result = await self._session.execute(stmt)
        rows = result.mappings().all()

        return [InboxMessage(**row) for row in rows]

    async def mark_processed(self, message_ids: list[UUID]) -> None:
        await self._session.execute(
            update(inbox_messages_table)
            .where(inbox_messages_table.c.message_id.in_(message_ids))
            .values(processed_at=datetime.now(UTC))
        )

    async def _exists(self, message_id: UUID) -> bool:
        stmt = select(inbox_messages_table.c.message_id).where(
            inbox_messages_table.c.message_id == message_id
        )
        result = await self._session.execute(stmt)
        return result.scalar() is not None
