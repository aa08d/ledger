from dataclasses import dataclass
from uuid import UUID

from ledger.domain.ledger.repository import LedgerRepository
from ledger.application.common.commands import Command, CommandHandler
from ledger.application.common.interfaces import Mediator, UnitOfWork
from ledger.application.ledger.interfaces import Outbox
from ledger.domain.ledger.value_objects import LedgerID, LedgerReason
from ledger.application.ledger.exceptions import LedgerNotFoundException


@dataclass(frozen=True)
class FailLedgerCommand(Command):
    ledger_id: UUID
    code: str
    details: str


class FailLedgerHandler(CommandHandler[None]):
    def __init__(
        self,
        repository: LedgerRepository,
        mediator: Mediator,
        outbox: Outbox,
        uow: UnitOfWork,
    ) -> None:
        self._repository = repository
        self._mediator = mediator
        self._uow = uow
        self._outbox = outbox

    async def __call__(self, command: FailLedgerCommand) -> None:
        ledger = await self._repository.acquire_by_id(
            LedgerID(command.ledger_id),
        )

        if ledger is None:
            raise LedgerNotFoundException(command.ledger_id)

        ledger.fail(LedgerReason(command.code, command.details))
        events = ledger.pull_events()

        await self._repository.save(ledger)
        await self._mediator.publish(events)
        await self._outbox.append(events)
        await self._uow.commit()
