from dataclasses import dataclass

from fastapi import APIRouter, status


router = APIRouter(prefix="/healthcheck", tags=["healthcheck"])


@dataclass(frozen=True)
class OKStatus:
    code: int = 200
    message: str = "OK"


@router.get("", status_code=status.HTTP_200_OK)
async def healthcheck() -> OKStatus:
    return OKStatus()
