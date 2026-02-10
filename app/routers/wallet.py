from fastapi import APIRouter, Header, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.models.wallet import Wallet
from uuid import UUID

router = APIRouter()

@router.get("/wallet/balance")
async def get_balance(client_id: UUID = Header(...), db: AsyncSession = Depends(get_db)):
    wallet = await db.get(Wallet, client_id)
    return {"balance": wallet.balance if wallet else 0}