"""
Setup sqlite db for tests
"""
from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app import crud
from app.db.base_class import Base
from app.helpers.db import get_db
from app.main import app
from app.schemas import AccountSchema, OrderSchema

DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

Base.metadata.create_all(bind=engine)  # type: ignore[attr-defined]

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture(scope="session")
def db() -> Generator:
    session = TestingSessionLocal()
    yield session
    session.close()


@pytest.fixture(scope="session")
def client() -> Generator:
    """Override test client with local db

    Yields:
        Generator: TestClient
    """
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c


@pytest.fixture
def account(db: Session):
    item_in = AccountSchema(cash=100)
    account = crud.account.create(db=db, obj_in=item_in)
    return account


@pytest.fixture
def order_schema(account):
    return OrderSchema(
        timestamp=1571325625,
        operation="BUY",
        issuer_name="AAPL",
        total_shares=2,
        share_price=50,
        account_id=account.id,
    )
