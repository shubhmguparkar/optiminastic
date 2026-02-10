
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.core.database import get_db
from app.models.wallet import Wallet
from app.models.ledger import WalletLedger
from app.schemas.admin import WalletCreditRequest
from app.schemas.admin import WalletDebitRequest


router = APIRouter(prefix="/admin", tags=["Admin"])

@router.post("/wallet/credit")
async def credit_wallet(
    payload: WalletCreditRequest,
    db: AsyncSession = Depends(get_db)
):
    if payload.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be positive")

    async with db.begin():
        wallet = await db.get(Wallet, payload.client_id)

        if not wallet:
            wallet = Wallet(client_id=payload.client_id, balance=0)
            db.add(wallet)

        wallet.balance += payload.amount

        db.add(
            WalletLedger(
                client_id=payload.client_id,
                type="CREDIT",
                amount=payload.amount,
                reference_type="ADMIN"
            )
        )

    return {
        "status": "credited",
        "balance": wallet.balance
    }


@router.post("/wallet/debit")
async def debit_wallet(
    payload: WalletDebitRequest,
    db: AsyncSession = Depends(get_db)
):
    if payload.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be positive")

    async with db.begin():
        wallet = await db.get(Wallet, payload.client_id)

        if not wallet:
            raise HTTPException(status_code=404, detail="Wallet not found")

        if wallet.balance < payload.amount:
            raise HTTPException(status_code=400, detail="Insufficient balance")

        wallet.balance -= payload.amount

        db.add(
            WalletLedger(
                client_id=payload.client_id,
                type="DEBIT",
                amount=payload.amount,
                reference_type="ADMIN"
            )
        )

    return {
        "status": "debited",
        "balance": wallet.balance
    }
