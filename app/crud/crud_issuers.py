from typing import Optional

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.issuers import Issuer
from app.schemas.issuers import IssuerSchema


class CRUDIssuer(CRUDBase[Issuer, IssuerSchema]):
    """Issuer CRUD class"""

    def get_issuer_by_name(
        self, db: Session, account_id: int, name: str
    ) -> Optional[Issuer]:
        """Return Account issuer by name"""
        return (
            db.query(self.model)
            .filter(Issuer.account_id == account_id, Issuer.issuer_name == name)
            .first()
        )


issuer = CRUDIssuer(Issuer)
