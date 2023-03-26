import datetime
from typing import List, Optional

import pytz  # type: ignore[import]
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from app import crud
from app.business_logic import constans
from app.models.accounts import Account
from app.schemas import OrderSchema
from app.utils.exceptions import InvalidAccount


class BaseManager:
    def __init__(self, db: Session, account_id: int):
        self._db = db
        try:
            self._account = crud.account.get(db=db, id=account_id)
        except NoResultFound:
            raise InvalidAccount

        self._redis = None
        self.errors: List[str] = []

    @property
    def account(self) -> Optional[Account]:
        self._db.refresh(self._account)
        return self._account

    @staticmethod
    def _is_market_open() -> bool:
        current_datetime = datetime.datetime.now(pytz.timezone(constans.TIMEZONE))
        if current_datetime.weekday() not in constans.OPEN_MARKET_DAYS_OF_WEEK:
            return False

        current_time = current_datetime.time()
        return constans.OPEN_MARKET_TIME < current_time < constans.CLOSE_MARKET_TIME

    def _is_duplicated_operation(self) -> bool:
        self._redis = None
        return False

    def _can_be_processed(self, order: OrderSchema) -> bool:
        if order.operation not in constans.VALID_OPERATION_TYPES:
            self.errors.append(constans.INVALID_OPERATION)
            return False

        if not self._is_market_open():
            self.errors.append(constans.CLOSED_MARKET)
            return False

        if self._is_duplicated_operation():
            self.errors.append(constans.DUPLICATED_OPERATION)
            return False

        return True

    def process(self, order: OrderSchema) -> bool:
        if not self._can_be_processed(order=order):
            return False

        try:
            return self.__getattribute__(order.operation.lower())
        except AttributeError:
            self.errors.append(constans.INVALID_OPERATION)
            return False
