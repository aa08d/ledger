from fastapi import APIRouter, status

from fastapi.responses import RedirectResponse


router = APIRouter(
    prefix="",
    tags=["default"],
    include_in_schema=False,
)


@router.get("/")
async def default() -> RedirectResponse:
    return RedirectResponse(url="/docs", status_code=status.HTTP_302_FOUND)
