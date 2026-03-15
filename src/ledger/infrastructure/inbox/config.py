from dataclasses import dataclass


@dataclass(frozen=True)
class InboxConfig:
    host: str = "localhost"
    port: int = 5672
    username: str = "guest"
    password: str = "guest"
    queue: str = "inbox_events"
    prefetch_count: int = 10
    concurrency: int = 1
