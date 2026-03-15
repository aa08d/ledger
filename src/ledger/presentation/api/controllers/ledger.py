from uuid import UUID

from fastapi import APIRouter, Query
from dishka.integrations.fastapi import DishkaRoute, FromDishka

from ledger.domain.common.constants import Empty
from ledger.domain.ledger.value_objects import LedgerType, LedgerStatus, CurrencyCode
from ledger.application.common.interfaces import Mediator
from ledger.application.common.pagination import Pagination, SortOrder
from ledger.application.ledger.dto import LedgerDTO, LedgersDTO
from ledger.application.ledger.queries import (
    GetLedgerByIDQuery,
    GetLedgerByTransactionIDQuery,
    GetLedgersQuery,
)
from ledger.application.ledger.interfaces import LedgerFilters
from ledger.presentation.api.controllers.responses import OkResponse


router = APIRouter(
    prefix="/api/v1/ledger",
    tags=["ledger"],
    route_class=DishkaRoute,
)


@router.get("/{ledger_id}")
async def get_ledger(
    ledger_id: UUID,
    mediator: FromDishka[Mediator],
) -> OkResponse[LedgerDTO]:
    ledger = await mediator.send(GetLedgerByIDQuery(ledger_id))
    return OkResponse(result=ledger)


@router.get("transaction/{transaction_id}")
async def get_by_transaction(
    transaction_id: UUID,
    mediator: FromDishka[Mediator],
) -> OkResponse[LedgerDTO]:
    ledger = await mediator.send(GetLedgerByTransactionIDQuery(transaction_id))
    return OkResponse(result=ledger)


@router.get("")
async def get_ledgers(
    mediator: FromDishka[Mediator],
    wallet_id: UUID | None = None,
    ledger_type: LedgerType | None = None,
    status: LedgerStatus | None = None,
    currency: CurrencyCode | None = None,
    offset: int | None = Query(None, ge=0),
    limit: int | None = Query(None, ge=1, le=1000),
    order: SortOrder = SortOrder.ASC,
) -> OkResponse[LedgersDTO]:
    ledgers = await mediator.send(
        GetLedgersQuery(
            filters=LedgerFilters(
                wallet_id=wallet_id if wallet_id is not None else Empty.UNSET,
                type=ledger_type if ledger_type is not None else Empty.UNSET,
                status=status if status is not None else Empty.UNSET,
                currency=currency if currency is not None else Empty.UNSET,
            ),
            pagination=Pagination(
                offset=offset if offset is not None else Empty.UNSET,
                limit=limit if limit is not None else Empty.UNSET,
                order=order,
            ),
        )
    )

    return OkResponse(result=ledgers)
