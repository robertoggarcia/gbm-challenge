from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import schemas
from app.business_logic.orders import OperationsManager
from app.helpers.db import get_db
from app.schemas import OrderResponse
from app.schemas.issuers import BalancePayload, IssuerResponse
from app.utils.exceptions import InvalidAccount

router = APIRouter()


@router.post("/{account_id}/orders", response_model=schemas.OrderResponse)
def create_order(
    *,
    db: Session = Depends(get_db),
    account_id: int,
    order_in: schemas.OrderSchema,
) -> Any:
    """
    Create new order.
    """
    try:
        operator = OperationsManager(db=db, account_id=account_id)
        operator.process(order=order_in)
        account = operator.account

        return OrderResponse(
            current_balance=BalancePayload(
                cash=account.cash,
                issuers=[
                    IssuerResponse(**jsonable_encoder(issuer))
                    for issuer in account.issuers
                ],
            ),
            business_errors=operator.errors,
        )
    except InvalidAccount:
        raise HTTPException(status_code=404, detail="Account not found")
