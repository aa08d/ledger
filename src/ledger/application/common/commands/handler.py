from abc import ABC, abstractmethod

from .command import Command


class CommandHandler[CR](ABC):
    @abstractmethod
    async def __call__(self, command: Command) -> CR: ...
