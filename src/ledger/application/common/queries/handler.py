from abc import ABC, abstractmethod

from .query import Query


class QueryHandler[QR](ABC):
    @abstractmethod
    async def __call__(self, query: Query) -> QR: ...
