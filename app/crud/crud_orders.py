from app.crud.base import CRUDBase
from app.models.orders import Order
from app.schemas.orders import OrderSchema


class CRUDOrder(CRUDBase[Order, OrderSchema]):
    """Order CRUD class"""

    pass


order = CRUDOrder(Order)
