from typing import Any

from fastapi import APIRouter, Depends
from loguru import logger
from sqlalchemy.orm import Session

from app import crud, schemas
from app.helpers.db import get_db

router = APIRouter()


@router.post("/", response_model=schemas.Account)
def create_account(
    *,
    db: Session = Depends(get_db),
    account_in: schemas.AccountSchema,
) -> Any:
    """
    Create new account.
    """
    account = crud.account.create(db=db, obj_in=account_in)
    logger.debug(f"New account created: {account.id}")
    return account
