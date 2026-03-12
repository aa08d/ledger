from ledger.domain.common.events import Event
from .message import InboxMessage


def convert_inbox_message_to_integration_event(message: InboxMessage) -> Event | None:
    match message.event:
        case "create.ledger":
            pass
        case "confirm.ledger":
            pass
        case "fail.ledger":
            pass
        case _:
            return None
