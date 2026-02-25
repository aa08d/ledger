from abc import ABC, abstractmethod

from .command import Command


class CommandHandler[CResult](ABC):
    @abstractmethod
    async def __call__(self, command: Command) -> CResult:
        raise NotImplementedError
