from app.crud.base import CRUDBase
from app.models.accounts import Account
from app.schemas.accounts import AccountSchema


class CRUDAccount(CRUDBase[Account, AccountSchema]):
    """Account CRUD class"""

    pass


account = CRUDAccount(Account)
