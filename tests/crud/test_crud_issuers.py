import pytest
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from app import crud
from app.models.issuers import Issuer
from app.schemas import AccountSchema
from app.schemas.issuers import IssuerSchema


def test_create_issuer(db: Session) -> None:
    """Test create a valid issuer"""
    account = crud.account.create(db=db, obj_in=AccountSchema(cash=100))
    issuer_in = IssuerSchema(
        issuer_name="AAPL",
        total_shares=2,
        share_price=50,
        account_id=account.id,
    )
    issuer = crud.issuer.create(db=db, obj_in=issuer_in)

    issuer_created = db.query(Issuer).filter(Issuer.id == issuer.id).first()
    assert issuer_created.id == issuer.id


def test_get_issuer(db: Session) -> None:
    """Test get issuer"""
    account = crud.account.create(db=db, obj_in=AccountSchema(cash=100))
    issuer_in = IssuerSchema(
        issuer_name="AAPL",
        total_shares=2,
        share_price=50,
        account_id=account.id,
    )
    issuer = crud.issuer.create(db=db, obj_in=issuer_in)

    issuer_created = crud.issuer.get(db=db, id=issuer.id)
    assert issuer_created.id == issuer.id  # type: ignore[union-attr]


def test_get_issuer_not_found(db: Session) -> None:
    """Test NoResultFound"""
    with pytest.raises(NoResultFound):
        crud.issuer.get(db=db, id=0)


def test_update_issuer(db: Session) -> None:
    """Test update issuer"""
    account = crud.account.create(db=db, obj_in=AccountSchema(cash=100))
    issuer_in = IssuerSchema(
        issuer_name="AAPL",
        total_shares=2,
        share_price=50,
        account_id=account.id,
    )
    issuer = crud.issuer.create(db=db, obj_in=issuer_in)
    crud.issuer.update(db=db, db_obj=issuer, obj_in={"issuer_name": "updated name"})

    updated_issuer = crud.issuer.get(db=db, id=issuer.id)
    assert updated_issuer.id == issuer.id  # type: ignore[union-attr]
    assert updated_issuer.issuer_name == "updated name"  # type: ignore[union-attr]


def test_remove_issuer(db: Session) -> None:
    """Test remove issuer"""
    account = crud.account.create(db=db, obj_in=AccountSchema(cash=100))
    issuer_in = IssuerSchema(
        issuer_name="AAPL",
        total_shares=2,
        share_price=50,
        account_id=account.id,
    )
    issuer = crud.issuer.create(db=db, obj_in=issuer_in)

    crud.issuer.delete(db=db, id=issuer.id)

    with pytest.raises(NoResultFound):
        crud.issuer.get(db=db, id=issuer.id)
