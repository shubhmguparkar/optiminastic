from sqlalchemy import Column, Numeric, String, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from uuid import uuid4
from app.core.database import Base

class WalletLedger(Base):
    __tablename__ = "wallet_ledger"
    id = Column(UUID, primary_key=True, default=uuid4)
    client_id = Column(UUID)
    type = Column(Enum("CREDIT","DEBIT", name="ledger_type"))
    amount = Column(Numeric(12,2))
    reference_type = Column(String)
    reference_id = Column(UUID)
    created_at = Column(DateTime, server_default=func.now())