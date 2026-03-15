from dataclasses import dataclass

from ledger.infrastructure.inbox.config import InboxConfig
from ledger.infrastructure.outbox import OutboxConfig
from ledger.infrastructure.persistence.config import DBConfig
from ledger.infrastructure.logging.config import LoggingConfig
from ledger.presentation.api.config import APIConfig


@dataclass(frozen=True)
class Config:
    api: APIConfig
    database: DBConfig
    outbox: OutboxConfig
    inbox: InboxConfig
    logging: LoggingConfig
