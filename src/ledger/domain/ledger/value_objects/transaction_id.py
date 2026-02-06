from uuid import UUID

from ledger.domain.common.value_objects import ValueObject


class TransactionID(ValueObject):
    def __init__(self, uuid: UUID) -> None:
        self.uuid = uuid

    @property
    def value(self) -> UUID:
        return self.uuid
