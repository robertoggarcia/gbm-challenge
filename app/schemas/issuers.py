from typing import List, Optional

from pydantic import BaseModel


class IssuerBase(BaseModel):
    issuer_name: str
    total_shares: int
    share_price: float
    account_id: int


class IssuerSchema(IssuerBase):
    account_id: Optional[int]  # type: ignore[assignment]


class Issuer(IssuerBase):
    id: int
    timestamp: int
    operation: str
    issuer_name: str
    total_shares: int
    share_price: float
    account_id: int

    class Config:
        orm_mode = True


class IssuerResponse(BaseModel):
    issuer_name: str
    total_shares: int
    share_price: float


class BalancePayload(BaseModel):
    cash: float
    issuers: List[IssuerResponse]


class OrderResponse(BaseModel):
    current_balance: BalancePayload
    business_errors: List[str]
