from dataclasses import dataclass
from uuid import UUID

from ledger.domain.ledger.repository import LedgerRepository
from ledger.application.common.commands import Command, CommandHandler
from ledger.application.common.interfaces import Mediator, UnitOfWork
from ledger.application.ledger.interfaces import Outbox
from ledger.domain.ledger.entities import Ledger
from ledger.domain.ledger.value_objects import (
    WalletID,
    TransactionID,
    LedgerType,
    Amount,
    CurrencyCode,
    LedgerReason,
)


@dataclass(frozen=True)
class CreateLedgerCommand(Command):
    wallet_id: UUID
    transaction_id: UUID
    type: LedgerType
    amount: int
    currency: CurrencyCode
    code: str
    details: str


class CreateLedgerHandler(CommandHandler[UUID]):
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

    async def __call__(self, command: CreateLedgerCommand) -> UUID:
        ledger = Ledger.create(
            wallet_id=WalletID(command.wallet_id),
            transaction_id=TransactionID(command.transaction_id),
            ledger_type=command.type,
            amount=Amount(command.amount, command.currency),
            reason=LedgerReason(command.code, command.details),
        )
        events = ledger.pull_events()

        await self._repository.save(ledger)
        await self._mediator.publish(events)
        await self._outbox.append(events)
        await self._uow.commit()

        return ledger.id.value
