from fastapi import APIRouter, Depends, status

from app.api.api_V1.endpoints import accounts, orders
from app.utils import auth

api_router = APIRouter()

api_router.include_router(
    accounts.router,
    prefix="/accounts",
    dependencies=[Depends(auth.validate_token)],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}},
)
api_router.include_router(
    orders.router,
    prefix="/accounts",
    dependencies=[Depends(auth.validate_token)],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}},
)
