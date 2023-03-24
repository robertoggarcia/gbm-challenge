from pydantic import BaseModel


class AccountBase(BaseModel):
    cash: float


class AccountSchema(AccountBase):
    pass


class Account(AccountBase):
    id: int
    cash: float

    class Config:
        orm_mode = True
