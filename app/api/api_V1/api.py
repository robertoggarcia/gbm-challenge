from fastapi import APIRouter, status

from app.api.api_V1.endpoints import accounts, orders

api_router = APIRouter()

api_router.include_router(
    accounts.router,
    prefix="/accounts",
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}},
)
api_router.include_router(
    orders.router,
    prefix="/accounts",
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}},
)
