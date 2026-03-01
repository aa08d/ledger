from abc import ABC
from typing import List

from ledger.domain.common.events import Event


class AggregateRoot(ABC):
    def __init__(self) -> None:
        self._events: List[Event] = []

    def raise_event(self, event: Event) -> None:
        self._events.append(event)

    @property
    def domain_events(self) -> List[Event]:
        return self._events.copy()

    def clear_events(self) -> None:
        self._events.clear()

    def pull_events(self) -> List[Event]:
        events = self.domain_events
        self.clear_events()
        return events
