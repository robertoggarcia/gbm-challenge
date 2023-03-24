import datetime

from sqlalchemy import Column, DateTime, Float, Integer

from app.db.base_class import Base


class Account(Base):
    id = Column(Integer, primary_key=True, index=True)
    cash = Column(Float)

    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(
        DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow
    )
