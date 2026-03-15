from dishka import AsyncContainer

from ledger.application.common.interfaces import Mediator
from ledger.infrastructure.mediator import MediatorImpl
from ledger.application.ledger.commands import (
    CreateLedgerCommand,
    CreateLedgerHandler,
    ConfirmLedgerCommand,
    ConfirmLedgerHandler,
    FailLedgerCommand,
    FailLedgerHandler,
)
from ledger.application.ledger.queries import (
    GetLedgerByIDQuery,
    GetLedgersByIDHandler,
    GetLedgerByTransactionIDQuery,
    GetLedgersByTransactionIDHandler,
    GetLedgersQuery,
    GetLedgersHandler,
)


def init_mediator(container: AsyncContainer) -> Mediator:
    return MediatorImpl(container)


def setup_mediator(mediator: Mediator) -> None:
    mediator.register(CreateLedgerCommand, CreateLedgerHandler)
    mediator.register(ConfirmLedgerCommand, ConfirmLedgerHandler)
    mediator.register(FailLedgerCommand, FailLedgerHandler)
    mediator.register(GetLedgerByIDQuery, GetLedgersByIDHandler)
    mediator.register(GetLedgerByTransactionIDQuery, GetLedgersByTransactionIDHandler)
    mediator.register(GetLedgersQuery, GetLedgersHandler)
