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
            logger.info(f"Invalid account {account_id}")
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
        """Validate is market is open based on OPEN_MARKET_TIME, CLOSE_MARKET_TIME and OPEN_MARKET_DAYS_OF_WEEK"""
        current_datetime = datetime.datetime.now(pytz.timezone(constans.TIMEZONE))
        if current_datetime.weekday() not in constans.OPEN_MARKET_DAYS_OF_WEEK:
            return False

        current_time = current_datetime.time()
        return constans.OPEN_MARKET_TIME < current_time < constans.CLOSE_MARKET_TIME

    def _is_duplicated_operation(self, order: OrderSchema) -> bool:
        """Validate if the operation was duplicated in the defined window (5 minutes):
        account, operation, issuer, total_shares
        """
        if not self._in_memory_store:
            logger.error(f"Duplicated operation can't be validated: {order}")
            return not constans.ALLOW_DUPLICATION_IF_REDIS_FAILS

        key = f"{self._account.id}_{order.operation}_{order.issuer_name}_{order.total_shares}"
        order_duplicated = self._in_memory_store.get(key=key)

        return True if order_duplicated else False

    def _update_operation_in_memory(self, order: OrderSchema) -> None:
        """Set up last operation in memory: account, operation, issuer, total_shares. To avoid duplicated operations"""
        key = f"{self._account.id}_{order.operation}_{order.issuer_name}_{order.total_shares}"
        self._in_memory_store.set(key=key, value=order.dict())

    def _valid_share_values(self, order: OrderSchema) -> None:
        """Validate allowed shares values"""
        if order.total_shares < constans.DEFAULT_MIN_SHARES_VALUES:
            self.errors.append(constans.INVALID_TOTAL_SHARES_VALUE)

        if order.share_price < constans.DEFAULT_MIN_SHARES_VALUES:
            self.errors.append(constans.INVALID_SHARE_PRICE_VALUE)

    def _can_be_processed(self, order: OrderSchema) -> bool:
        """Validate business rules before execute an operation"""
        if order.operation not in constans.VALID_OPERATION_TYPES:
            self.errors.append(constans.INVALID_OPERATION)

        if not self._is_market_open():
            self.errors.append(constans.CLOSED_MARKET)

        if self._is_duplicated_operation(order=order):
            self.errors.append(constans.DUPLICATED_OPERATION)

        self._valid_share_values(order=order)

        return not self.errors

    def process(self, order: OrderSchema) -> bool:
        """Process operation"""
        if not self._can_be_processed(order=order):
            logger.info(f"Order can't be processed {order}: {self.errors}")
            return False

        try:
            result = self.__getattribute__(order.operation.lower())(order=order)
            logger.debug(f"{order}")
            if result:
                self._update_operation_in_memory(order=order)
            return result
        except AttributeError:
            self.errors.append(constans.INVALID_OPERATION)
            return False
