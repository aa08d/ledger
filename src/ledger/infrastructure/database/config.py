from dataclasses import dataclass


@dataclass
class DBConfig:
    host: str = "localhost"
    port: int = 5432
    database: str = "ledger"
    user: str = "postgres"
    password: str = ""
    echo: bool = True

    @property
    def full_url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"
