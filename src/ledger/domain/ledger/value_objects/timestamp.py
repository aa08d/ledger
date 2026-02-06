from datetime import datetime, UTC
from typing import Self

from ledger.domain.common.value_objects import ValueObject


class LedgerTimestamp(ValueObject):
    def __init__(self, created_at: datetime, updated_at: datetime) -> None:
        self._created_at = created_at
        self._updated_at = updated_at

    @classmethod
    def create(cls) -> Self:
        now = datetime.now(UTC)
        return cls(now, now)

    def update(self) -> Self:
        updated_at = datetime.now(UTC)
        return LedgerTimestamp(self._created_at, updated_at)

    @property
    def created_at(self) -> datetime:
        return self._created_at

    @property
    def updated_at(self) -> datetime:
        return self._updated_at
