from app import crud
from app.business_logic import constans
from app.business_logic.base_manager import BaseManager
from app.schemas import OrderSchema
from app.schemas.issuers import IssuerSchema


class OperationsManager(BaseManager):
    """Class to define business logic for all valid operations"""

    def buy(self, order: OrderSchema) -> bool:
        total = order.total_shares * order.share_price
        if total > self._account.cash:
            self.errors.append(constans.INSUFFICIENT_BALANCE)
            return False

        order.account_id = self._account.id
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
        issuer = crud.issuer.get_issuer_by_name(
            db=self._db, account_id=self._account.id, name=order.issuer_name
        )

        if issuer:
            current_stocks = issuer.total_shares

            if current_stocks < order.total_shares:
                self.errors.append(constans.INSUFFICIENT_STOCKS)
                return False

            order.account_id = self._account.id
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
            return False

        return True
