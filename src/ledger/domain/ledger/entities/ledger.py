from typing import Self

from ledger.domain.common.entities import Entity, AggregateRoot
from ledger.domain.ledger.value_objects import (
    LedgerID,
    WalletID,
    TransactionID,
    LedgerType,
    Amount,
    LedgerStatus,
    LedgerReason,
)
from ledger.domain.ledger.events import LedgerCreated, LedgerConfirmed, LedgerFailed
from ledger.domain.ledger.exceptions import (
    LedgerAlreadyConfirmed,
    LedgerAlreadyFailed,
    LedgerCannotTransition,
)


class Ledger(Entity, AggregateRoot):
    def __init__(
        self,
        ledger_id: LedgerID,
        wallet_id: WalletID,
        transaction_id: TransactionID,
        ledger_type: LedgerType,
        amount: Amount,
        status: LedgerStatus,
        reason: LedgerReason,
    ) -> None:
        super().__init__()
        self.id = ledger_id
        self.wallet_id = wallet_id
        self.transaction_id = transaction_id
        self.type = ledger_type
        self.amount = amount
        self.status = status
        self.reason = reason

    @classmethod
    def create(
        cls,
        wallet_id: WalletID,
        transaction_id: TransactionID,
        ledger_type: LedgerType,
        amount: Amount,
        reason: LedgerReason,
    ) -> Self:
        ledger_id = LedgerID.create()
        status = LedgerStatus.PENDING

        ledger = cls(
            ledger_id=ledger_id,
            wallet_id=wallet_id,
            transaction_id=transaction_id,
            ledger_type=ledger_type,
            amount=amount,
            status=status,
            reason=reason,
        )

        ledger.raise_event(
            LedgerCreated(
                ledger_id=ledger.id.value,
                wallet_id=ledger.wallet_id.value,
                transaction_id=ledger.transaction_id.value,
                type=ledger.type,
                amount=ledger.amount.value,
                currency=ledger.amount.currency,
                status=ledger.status,
                reason=ledger.reason.value,
            )
        )

        return ledger

    def confirm(self) -> None:
        if self.status == LedgerStatus.CONFIRMED:
            raise LedgerAlreadyConfirmed(ledger_id=self.id.value)

        if self.status != LedgerStatus.PENDING:
            raise LedgerCannotTransition(
                ledger_id=self.id.value,
                from_status=self.status,
                to_status=LedgerStatus.CONFIRMED,
            )

        self.status = LedgerStatus.CONFIRMED

        self.raise_event(
            LedgerConfirmed(
                ledger_id=self.id.value,
                wallet_id=self.wallet_id.value,
                transaction_id=self.transaction_id.value,
                type=self.type,
                amount=self.amount.value,
                currency=self.amount.currency,
                status=self.status,
                reason=self.reason.value,
            )
        )

    def fail(self, reason: LedgerReason) -> None:
        if self.status == LedgerStatus.FAILED:
            raise LedgerAlreadyFailed(ledger_id=self.id.value)

        if self.status != LedgerStatus.PENDING:
            raise LedgerCannotTransition(
                ledger_id=self.id.value,
                from_status=self.status,
                to_status=LedgerStatus.FAILED,
            )

        self.status = LedgerStatus.FAILED
        self.reason = reason

        self.raise_event(
            LedgerFailed(
                ledger_id=self.id.value,
                wallet_id=self.wallet_id.value,
                transaction_id=self.transaction_id.value,
                type=self.type,
                amount=self.amount.value,
                currency=self.amount.currency,
                status=self.status,
                reason=self.reason.value,
            )
        )
