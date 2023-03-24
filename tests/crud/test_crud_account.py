from sqlalchemy.orm import Session

from app import crud
from app.models.accounts import Account
from app.schemas.accounts import AccountSchema


def test_create_account(db: Session) -> None:
    """Test create a valid account"""
    item_in = AccountSchema(cash=100)
    account = crud.account.create(db=db, obj_in=item_in)

    account_created = db.query(Account).filter(Account.id == account.id).first()
    assert account_created.id == account.id
