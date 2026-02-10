from pydantic import BaseModel
from uuid import UUID
from decimal import Decimal

class WalletCreditRequest(BaseModel):
    client_id: UUID
    amount: Decimal

class WalletDebitRequest(BaseModel):
    client_id: UUID
    amount: Decimal
