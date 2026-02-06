from uuid import UUID

from uuid6 import uuid7

from ledger.domain.common.value_objects import ValueObject


class LedgerID(ValueObject):
    def __init__(self, uuid: UUID) -> None:
        self.uuid = uuid

    @property
    def value(self) -> UUID:
        return self.uuid

    @classmethod
    def create(cls) -> 'LedgerID':
        return cls(uuid7())
