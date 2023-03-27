import datetime
from typing import List

import pytz  # type: ignore[import]
from loguru import logger
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from app import crud
from app.business_logic import constans
from app.db.in_memory import InMemoryManager
from app.models.accounts import Account
from app.schemas import OrderSchema
from app.utils.exceptions import InMemoryManagerConnectionError, InvalidAccount


class OperationInMemoryManager(InMemoryManager[str, dict]):
    salt = "OPERATIONS"
    lifetime = 60 * constans.DEFAULT_STOCK_OPERATION_VALID_MINUTES


class BaseManager:
    """
    Base class to set up business logic rules to validate
    before process an operation
    """

    def __init__(self, db: Session, account_id: int):
        self._db = db
        try:
            self._account = crud.account.get(db=db, id=account_id)
        except NoResultFound:
            raise InvalidAccount

        try:
            self._in_memory_store = OperationInMemoryManager()
        except InMemoryManagerConnectionError:
            self._in_memory_store = None  # type: ignore[assignment]

        self.errors: List[str] = []

    @property
    def account(self) -> Account:
        self._db.refresh(self._account)
        return self._account

    @staticmethod
    def _is_market_open() -> bool:
        current_datetime = datetime.datetime.now(pytz.timezone(constans.TIMEZONE))
        if current_datetime.weekday() not in constans.OPEN_MARKET_DAYS_OF_WEEK:
            return False

        current_time = current_datetime.time()
        return constans.OPEN_MARKET_TIME < current_time < constans.CLOSE_MARKET_TIME

    def _is_duplicated_operation(self, order: OrderSchema) -> bool:
        if not self._in_memory_store:
            logger.error(
                f"Duplicated operation can't be validated: "
                f"Account {self._account.id} Order {order.operation} "
                f"Issuer {order.issuer_name} Total shares {order.total_shares}"
            )
            return False

        key = f"{self._account.id}_{order.operation}_{order.issuer_name}_{order.total_shares}"
        order_duplicated = self._in_memory_store.get(key=key)

        return True if order_duplicated else False

    def _update_operation_in_memory(self, order: OrderSchema) -> None:
        key = f"{self._account.id}_{order.operation}_{order.issuer_name}_{order.total_shares}"
        self._in_memory_store.set(key=key, value=order.dict())

    def _valid_share_values(self, order: OrderSchema) -> bool:
        if order.total_shares < 0:
            self.errors.append(constans.INVALID_TOTAL_SHARES_VALUE)
            return False
        if order.share_price < 0:
            self.errors.append(constans.INVALID_SHARE_PRICE_VALUE)
            return False
        return True

    def _can_be_processed(self, order: OrderSchema) -> bool:
        if order.operation not in constans.VALID_OPERATION_TYPES:
            self.errors.append(constans.INVALID_OPERATION)
            return False

        if not self._is_market_open():
            self.errors.append(constans.CLOSED_MARKET)
            return False

        if self._is_duplicated_operation(order=order):
            self.errors.append(constans.DUPLICATED_OPERATION)
            return False

        if not self._valid_share_values(order=order):
            return False

        return True

    def process(self, order: OrderSchema) -> bool:
        if not self._can_be_processed(order=order):
            logger.error(
                f"Order can't be processed. Account id {self._account.id}, Operation {order.operation}: {self.errors}"
            )
            return False

        try:
            logger.debug(f"Account: {self._account.id} Operation: {order.operation}")
            self._update_operation_in_memory(order=order)
            return self.__getattribute__(order.operation.lower())(order=order)
        except AttributeError:
            self.errors.append(constans.INVALID_OPERATION)
            return False
