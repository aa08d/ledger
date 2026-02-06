from enum import StrEnum

from ledger.domain.common.value_objects import ValueObject


class CurrencyCode(StrEnum):
    COIN = "COIN"


class Amount(ValueObject):
    def __init__(self, amount: int, currency: CurrencyCode) -> None:
        self._amount = amount
        self._currency = currency

    @property
    def value(self) -> int:
        return self._amount

    @property
    def currency(self) -> CurrencyCode:
        return self._currency
