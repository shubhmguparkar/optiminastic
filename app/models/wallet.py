from sqlalchemy import Column, Numeric, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.core.database import Base

class Wallet(Base):
    __tablename__ = "wallets"
    client_id = Column(UUID, primary_key=True)
    balance = Column(Numeric(12,2), default=0)
    updated_at = Column(DateTime, server_default=func.now())