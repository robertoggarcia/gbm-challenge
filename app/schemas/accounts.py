from typing import List

from pydantic import BaseModel


class AccountBase(BaseModel):
    cash: float


class AccountSchema(AccountBase):
    pass


class Account(AccountBase):
    id: int
    cash: float
    issuers: List

    class Config:
        orm_mode = True
