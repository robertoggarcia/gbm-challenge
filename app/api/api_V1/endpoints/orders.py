from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import schemas
from app.business_logic.orders import OperationsManager
from app.helpers.db import get_db
from app.utils.exceptions import InvalidAccount
from app.utils.serializers import serialize_operation

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
        return serialize_operation(operation=operator)

    except InvalidAccount:
        raise HTTPException(status_code=404, detail="Account not found")
