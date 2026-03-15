from dataclasses import dataclass, field


@dataclass(frozen=True)
class Response:
    pass


@dataclass(frozen=True)
class OkResponse[Result](Response):
    status: int = 200
    result: Result | None = None


@dataclass(frozen=True)
class ExceptionData[Exception]:
    message: str = "Unknown error occurred"
    data: Exception | None = None


@dataclass(frozen=True)
class ExceptionResponse[Exception](Response):
    status: int = 500
    exception: ExceptionData[Exception] = field(default_factory=ExceptionData)
