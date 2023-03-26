from sqlalchemy.orm import Session

from app import crud
from app.business_logic import constans
from app.business_logic.orders import OperationsManager
from app.models.issuers import Issuer
from app.models.orders import Order
from app.schemas.issuers import IssuerSchema


def test_operations_manager_buy(db: Session, account, order_schema):
    new_balance = account.cash - (order_schema.total_shares * order_schema.share_price)

    operator = OperationsManager(db=db, account_id=account.id)
    process = operator.buy(order=order_schema)
    account_updated = operator.account

    assert process
    assert account_updated.cash == new_balance
    assert db.query(Order).filter(Order.account_id == account.id).first()
    assert len(db.query(Issuer).filter(Issuer.account_id == account.id).all()) == 1


def test_operations_manager_buy_insufficient_balance(
    db: Session, account, order_schema
):
    order_schema.total_shares = 10
    order_schema.share_price = 100

    operator = OperationsManager(db=db, account_id=account.id)
    process = operator.buy(order=order_schema)

    assert not process
    assert operator.errors == [constans.INSUFFICIENT_BALANCE]
    assert not db.query(Order).filter(Order.account_id == account.id).first()
    assert not db.query(Issuer).filter(Issuer.account_id == account.id).first()


def test_operations_manager_buy_existing_issuer(db: Session, account, order_schema):
    new_balance = account.cash - (order_schema.total_shares * order_schema.share_price)
    crud.issuer.create(
        db=db,
        obj_in=IssuerSchema(
            issuer_name=order_schema.issuer_name,
            total_shares=10,
            share_price=5,
            account_id=account.id,
        ),
    )

    operator = OperationsManager(db=db, account_id=account.id)
    process = operator.buy(order=order_schema)
    account_updated = operator.account
    issuer = db.query(Issuer).filter(Issuer.account_id == account.id).first()

    assert process
    assert account_updated.cash == new_balance
    assert db.query(Order).filter(Order.account_id == account.id).first()
    assert issuer.total_shares == 10 + order_schema.total_shares
    assert issuer.share_price == order_schema.share_price


def test_operations_manager_sell(db: Session, account, order_schema):
    new_balance = account.cash + (order_schema.total_shares * order_schema.share_price)
    crud.issuer.create(
        db=db,
        obj_in=IssuerSchema(
            issuer_name=order_schema.issuer_name,
            total_shares=10,
            share_price=5,
            account_id=account.id,
        ),
    )

    operator = OperationsManager(db=db, account_id=account.id)
    process = operator.sell(order=order_schema)
    account_updated = operator.account
    issuer = db.query(Issuer).filter(Issuer.account_id == account.id).first()

    assert process
    assert account_updated.cash == new_balance
    assert db.query(Order).filter(Order.account_id == account.id).first()
    assert issuer.total_shares == 10 - order_schema.total_shares
    assert issuer.share_price == order_schema.share_price


def test_operations_manager_sell_without_issuer(db: Session, account, order_schema):
    operator = OperationsManager(db=db, account_id=account.id)
    process = operator.sell(order=order_schema)

    assert not process
    assert operator.errors == [constans.INSUFFICIENT_STOCKS]


def test_operations_manager_sell_all(db: Session, account, order_schema):
    new_balance = account.cash + (order_schema.total_shares * order_schema.share_price)
    crud.issuer.create(
        db=db,
        obj_in=IssuerSchema(
            issuer_name=order_schema.issuer_name,
            total_shares=2,
            share_price=5,
            account_id=account.id,
        ),
    )

    operator = OperationsManager(db=db, account_id=account.id)
    process = operator.sell(order=order_schema)
    account_updated = operator.account
    issuer = db.query(Issuer).filter(Issuer.account_id == account.id).first()

    assert process
    assert account_updated.cash == new_balance
    assert db.query(Order).filter(Order.account_id == account.id).first()
    assert not issuer
