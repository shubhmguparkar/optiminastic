from sqlalchemy import Column, Numeric, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from uuid import uuid4
from decimal import Decimal
from app.core.database import Base

class Order(Base):
    __tablename__ = "orders"
    id = Column(UUID, primary_key=True, default=uuid4)
    client_id = Column(UUID)
    amount = Column(Numeric(12,2))
    status = Column(String)
    fulfillment_id = Column(String)
    created_at = Column(DateTime, server_default=func.now())