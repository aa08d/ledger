from typing import ClassVar


class AppException(Exception):
    status: ClassVar[int] = 500

    @property
    def message(self) -> str:
        return "An app exception occurred."


class DomainException(AppException):
    @property
    def message(self) -> str:
        return "A domain exception occurred."
