from typing import Optional

from pydantic import BaseModel


class OrderBase(BaseModel):
    timestamp: int
    operation: str
    issuer_name: str
    total_shares: int
    share_price: float
    account_id: int

    def __str__(self):
        return (
            f"Account {self.account_id} - Operation {self.operation} - Issuer {self.issuer_name} - "
            f"Shares {self.total_shares} - Share price {self.share_price}"
        )


class OrderSchema(OrderBase):
    account_id: Optional[int]  # type: ignore[assignment]


class Order(OrderBase):
    id: int
    timestamp: int
    operation: str
    issuer_name: str
    total_shares: int
    share_price: float
    account_id: int

    class Config:
        orm_mode = True
