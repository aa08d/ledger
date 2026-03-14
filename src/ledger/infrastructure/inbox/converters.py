from uuid import UUID

from ledger.application.common.commands import Command
from ledger.application.ledger.commands import CreateLedgerCommand, ConfirmLedgerCommand, FailLedgerCommand
from ledger.domain.ledger.value_objects import LedgerType, CurrencyCode

from .message import InboxMessage


def convert_inbox_message_to_command(message: InboxMessage) -> Command | None:
    match message.event:
        case "create.ledger":
            return CreateLedgerCommand(
                wallet_id=UUID(message.payload["wallet_id"]),
                transaction_id=UUID(message.payload["transaction_id"]),
                type=LedgerType(message.payload["type"]),
                amount=int(message.payload["amount"]),
                currency=CurrencyCode(message.payload["currency"]),
                code=message.payload["code"],
                details=message.payload.get("details", ""),
            )
        case "confirm.ledger":
            return ConfirmLedgerCommand(
                ledger_id=UUID(message.payload["ledger_id"]),
            )
        case "fail.ledger":
            return FailLedgerCommand(
                ledger_id=UUID(message.payload["ledger_id"]),
                code=message.payload["code"],
                details=message.payload.get("details", ""),
            )
        case _:
            return None
