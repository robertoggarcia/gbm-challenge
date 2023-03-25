import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, Text

from app.db.base_class import Base


class Issuer(Base):
    id = Column(Integer, primary_key=True, index=True)
    issuer_name = Column(Text, nullable=False)
    total_shares = Column(Integer)
    share_price = Column(Float)
    account_id = Column(Integer, ForeignKey("accounts.id"))

    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(
        DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow
    )
