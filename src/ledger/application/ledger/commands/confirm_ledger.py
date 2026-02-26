from dataclasses import dataclass
from uuid import UUID

from ledger.domain.ledger.repository import LedgerRepository
from ledger.application.common.commands import Command, CommandHandler
from ledger.application.common.interfaces import Mediator, UnitOfWork
from ledger.application.ledger.interfaces import Outbox
from ledger.domain.ledger.value_objects import LedgerID
from ledger.application.ledger.exceptions import LedgerNotFoundException


@dataclass(frozen=True)
class ConfirmLedgerCommand(Command):
    ledger_id: UUID


class ConfirmLedgerHandler(CommandHandler[None]):
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

    async def __call__(self, command: ConfirmLedgerCommand) -> None:
        ledger = await self._repository.acquire_by_id(
            ledger_id=LedgerID(command.ledger_id),
        )

        if ledger is None:
            raise LedgerNotFoundException(ledger_id=command.ledger_id)

        ledger.confirm()
        events = ledger.pull_events()

        await self._repository.save(ledger)
        await self._mediator.publish(events)
        await self._outbox.append(events)
        await self._uow.commit()
