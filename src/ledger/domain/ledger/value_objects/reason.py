from ledger.domain.common.value_objects import ValueObject


class LedgerReason(ValueObject):
    def __init__(self, code: str, details: str = "") -> None:
        self._code = code
        self._details = details

    @property
    def code(self) -> str:
        return self._code

    @property
    def details(self) -> str:
        return self._details

    @property
    def value(self) -> str:
        return f'{self._code}:{self._details}'
