from datetime import datetime, UTC
from uuid import UUID

from sqlalchemy import select, insert, update
from sqlalchemy.ext.asyncio import AsyncSession

from ledger.application.ledger.interfaces import Inbox
from ledger.application.ledger.dto import InboxMessageDTO

from .model import inbox_messages_table


class SQLAlchemyInbox(Inbox):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def exists(self, message_id: UUID) -> bool:
        stmt = select(inbox_messages_table.c.message_id).where(
            inbox_messages_table.c.message_id == message_id
        )
        result = await self._session.execute(stmt)
        return result.scalar() is not None

    async def save(self, message: InboxMessageDTO) -> None:
        await self._session.execute(
            insert(inbox_messages_table).values(
                message_id=message.message_id,
                event=message.event,
                payload=message.payload,
            )
        )

    async def done(self, message_id: UUID) -> None:
        await self._session.execute(
            update(inbox_messages_table)
            .where(inbox_messages_table.c.message_id == message_id)
            .values(processed_at=datetime.now(UTC))
        )
