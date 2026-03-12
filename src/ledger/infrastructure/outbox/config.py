from dataclasses import dataclass


@dataclass(frozen=True)
class OutboxConfig:
    batch_size: int = 100
    poll_interval: float = 1.0
