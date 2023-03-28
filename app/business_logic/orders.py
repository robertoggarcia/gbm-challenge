from loguru import logger

from app import crud
from app.business_logic import constans
from app.business_logic.base_manager import BaseManager
from app.schemas import OrderSchema
from app.schemas.issuers import IssuerSchema


class OperationsManager(BaseManager):
    """Class to define business logic for all valid operations"""

    def buy(self, order: OrderSchema) -> bool:
        """Buy issuer and add to account"""
        order.account_id = self._account.id
        total = order.total_shares * order.share_price
        if total > self._account.cash:
            self.errors.append(constans.INSUFFICIENT_BALANCE)
            logger.info(f"Order can't be processed {order}: {self.errors}")
            return False

        crud.order.create(db=self._db, obj_in=order)
        issuer = crud.issuer.get_issuer_by_name(
            db=self._db, account_id=self._account.id, name=order.issuer_name
        )
        if issuer:
            crud.issuer.update(
                db=self._db,
                db_obj=issuer,
                obj_in={
                    "total_shares": issuer.total_shares + order.total_shares,
                    "share_price": order.share_price,
                },
            )
        else:
            crud.issuer.create(db=self._db, obj_in=IssuerSchema(**order.dict()))

        new_balance = self._account.cash - (order.total_shares * order.share_price)
        crud.account.update(
            db=self._db, db_obj=self._account, obj_in={"cash": new_balance}
        )

        return True

    def sell(self, order: OrderSchema) -> bool:
        """Sell account issuer"""
        issuer = crud.issuer.get_issuer_by_name(
            db=self._db, account_id=self._account.id, name=order.issuer_name
        )
        order.account_id = self._account.id

        if issuer:
            current_stocks = issuer.total_shares

            if current_stocks < order.total_shares:
                logger.info(f"Order can't be processed {order}: {self.errors}")
                self.errors.append(constans.INSUFFICIENT_STOCKS)
                return False

            crud.order.create(db=self._db, obj_in=order)

            shares = issuer.total_shares - order.total_shares

            if shares > 0:
                crud.issuer.update(
                    db=self._db,
                    db_obj=issuer,
                    obj_in={"total_shares": shares, "share_price": order.share_price},
                )
            else:
                crud.issuer.delete(db=self._db, id=issuer.id)

            new_balance = self._account.cash + (order.total_shares * order.share_price)
            crud.account.update(
                db=self._db, db_obj=self._account, obj_in={"cash": new_balance}
            )
        else:
            self.errors.append(constans.INSUFFICIENT_STOCKS)
            logger.info(f"Order can't be processed {order}: {self.errors}")
            return False

        return True
