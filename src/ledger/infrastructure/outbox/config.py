from dataclasses import dataclass


@dataclass(frozen=True)
class OutboxConfig:
    host: str = "localhost"
    port: int = 5672
    username: str = "guest"
    password: str = "guest"
    exchange: str = "outbox_events"
    vhost: str = "/"
    batch_size: int = 100
    poll_interval: float = 1.0
