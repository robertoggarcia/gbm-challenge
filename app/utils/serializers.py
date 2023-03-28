from fastapi.encoders import jsonable_encoder

from app.business_logic.base_manager import BaseManager
from app.schemas import OrderResponse
from app.schemas.issuers import BalancePayload, IssuerResponse


def serialize_operation(operation: BaseManager) -> OrderResponse:
    """Serialize operation result to OrderResponse"""
    account = operation.account

    return OrderResponse(
        current_balance=BalancePayload(
            cash=account.cash,
            issuers=[
                IssuerResponse(**jsonable_encoder(issuer)) for issuer in account.issuers
            ],
        ),
        business_errors=operation.errors,
    )
