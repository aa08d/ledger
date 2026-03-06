from  typing import Any

from ledger.application.ledger.dto import LedgerDTO


def covert_ledger_row_to_dto(ledger: Any) -> LedgerDTO:
    return LedgerDTO(
        id=ledger.id,
        wallet_id=ledger.wallet.id,
        transaction_id=ledger.transaction.id,
        type=ledger.type,
        amount=ledger.amount,
        currency=ledger.currency,
        status=ledger.status,
        code=ledger.code,
        details=ledger.details,
    )
