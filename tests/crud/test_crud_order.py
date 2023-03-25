from sqlalchemy.orm import Session

from app import crud
from app.models.orders import Order
from app.schemas import AccountSchema
from app.schemas.orders import OrderSchema


def test_create_order(db: Session) -> None:
    """Test create a valid order"""
    account = crud.account.create(db=db, obj_in=AccountSchema(cash=100))
    order_in = OrderSchema(
        timestamp=1571325625,
        operation="BUY",
        issuer_name="AAPL",
        total_shares=2,
        share_price=50,
        account_id=account.id,
    )
    order = crud.order.create(db=db, obj_in=order_in)

    order_created = db.query(Order).filter(Order.id == order.id).first()
    assert order_created.id == order.id
