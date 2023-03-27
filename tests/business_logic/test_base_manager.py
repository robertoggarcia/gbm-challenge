from freezegun import freeze_time
from sqlalchemy.orm import Session

from app.business_logic import constans
from app.business_logic.base_manager import BaseManager, OperationInMemoryManager


@freeze_time("2023-03-27 12:00:00-06:00")
def test_base_manager_open_market(db: Session, account):
    base_manager = BaseManager(db=db, account_id=account.id)
    assert base_manager._is_market_open()


@freeze_time("2023-03-27 19:00:00-06:00")
def test_base_manager_open_market_false(db: Session, account):
    base_manager = BaseManager(db=db, account_id=account.id)
    assert not base_manager._is_market_open()


@freeze_time("2023-03-27 12:00:00-06:00")
def test_base_manager_can_be_processed_valid_op(db: Session, account, order_schema):
    base_manager = BaseManager(db=db, account_id=account.id)
    assert base_manager._can_be_processed(order=order_schema)
    assert not base_manager.errors


@freeze_time("2023-03-27 12:00:00-06:00")
def test_base_manager_can_be_processed_invalid_op(db: Session, account, order_schema):
    order_schema.operation = "test"
    base_manager = BaseManager(db=db, account_id=account.id)
    assert not base_manager._can_be_processed(order=order_schema)
    assert base_manager.errors == [constans.INVALID_OPERATION]


@freeze_time("2023-03-27 19:00:00-06:00")
def test_base_manager_can_be_processed_close_market(db: Session, account, order_schema):
    base_manager = BaseManager(db=db, account_id=account.id)
    assert not base_manager._can_be_processed(order=order_schema)
    assert base_manager.errors == [constans.CLOSED_MARKET]


@freeze_time("2023-03-27 12:00:00-06:00")
def test_base_manager_can_be_processed_invalid_total_shares(
    db: Session, account, order_schema
):
    order_schema.total_shares = -1
    base_manager = BaseManager(db=db, account_id=account.id)
    assert not base_manager._can_be_processed(order=order_schema)
    assert base_manager.errors == [constans.INVALID_TOTAL_SHARES_VALUE]


@freeze_time("2023-03-27 12:00:00-06:00")
def test_base_manager_can_be_processed_invalid_shares_price(
    db: Session, account, order_schema
):
    order_schema.share_price = -1
    base_manager = BaseManager(db=db, account_id=account.id)
    assert not base_manager._can_be_processed(order=order_schema)
    assert base_manager.errors == [constans.INVALID_SHARE_PRICE_VALUE]


@freeze_time("2023-03-27 12:00:00-06:00")
def test_base_manager_can_be_processed_duplicated_operation(
    db: Session, account, order_schema, in_memory_instance
):
    key = f"{account.id}_{order_schema.operation}_{order_schema.issuer_name}_{order_schema.total_shares}"
    in_memory_instance.set(f"{OperationInMemoryManager.salt}_{key}", 1, ex=60 * 2)

    base_manager = BaseManager(db=db, account_id=account.id)
    assert not base_manager._can_be_processed(order=order_schema)
    assert base_manager.errors == [constans.DUPLICATED_OPERATION]
