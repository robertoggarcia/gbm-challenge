from typing import List

from pydantic import BaseModel, validator

from app.business_logic.constans import MIN_OPEN_ACCOUNT_CASH_VALUE


class AccountBase(BaseModel):
    cash: float

    @validator("cash")
    def min_cash_value(cls, v):
        if v < MIN_OPEN_ACCOUNT_CASH_VALUE:
            raise ValueError(f"must be great that {MIN_OPEN_ACCOUNT_CASH_VALUE}")
        return v


class AccountSchema(AccountBase):
    pass


class Account(AccountBase):
    id: int
    cash: float
    issuers: List

    class Config:
        orm_mode = True
