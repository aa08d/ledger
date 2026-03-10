from ledger.domain.common.events import Event
from ledger.application.ledger.dto import InboxMessageDTO


def convert_inbox_message_to_integration_event(message: InboxMessageDTO) -> Event:
    match message.event:
        case _:
            ...
