from fastapi import APIRouter, Header, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.models.order import Order
from app.models.wallet import Wallet
from uuid import UUID
import httpx
from decimal import Decimal

router = APIRouter()

@router.post("/orders")
async def create_order(amount: float, client_id: UUID = Header(...), db: AsyncSession = Depends(get_db)):
    # Convert float to Decimal
    amount = Decimal(str(amount))

    # 1️⃣ Transaction: wallet deduction + order creation
    async with db.begin():
        wallet_result = await db.execute(select(Wallet).where(Wallet.client_id == client_id))
        wallet = wallet_result.scalar_one_or_none()
        if not wallet:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Wallet not found")
        
        if wallet.balance < amount:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Insufficient balance")
        
        wallet.balance -= amount
        db.add(wallet)
        
        order = Order(client_id=client_id, amount=amount, status="PENDING")
        db.add(order)

    # 2️⃣ Fulfillment API
    try:
        async with httpx.AsyncClient() as client:
            res = await client.post(
                "https://jsonplaceholder.typicode.com/posts",
                json={"userId": str(client_id), "title": str(order.id)}
            )
        res.raise_for_status()
        fulfillment_id = str(res.json()["id"])
    except Exception as e:
        # Refund wallet if API fails
        async with db.begin():
            wallet.balance += amount
            db.add(wallet)
            order.status = "FAILED"
            db.add(order)
        raise HTTPException(status_code=500, detail=f"Fulfillment API failed: {e}")

    # 3️⃣ Update order
    async with db.begin():
        order.fulfillment_id = fulfillment_id
        order.status = "FULFILLED"
        db.add(order)

    return {"order_id": order.id, "fulfillment_id": fulfillment_id, "status": order.status}


@router.get("/orders/{order_id}")
async def get_order(order_id: UUID, client_id: UUID = Header(...), db: AsyncSession = Depends(get_db)):
    # Fetch order from DB
    result = await db.execute(select(Order).where(Order.id == order_id))
    order = result.scalar_one_or_none()

    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    
    # Validate that this client owns the order
    if order.client_id != client_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to view this order")
    
    # Return order info
    return {
        "order_id": order.id,
        "amount": str(order.amount),         # Convert Decimal to str for JSON
        "status": order.status,
        "fulfillment_id": order.fulfillment_id,
        "created_at": order.created_at.isoformat() if order.created_at else None
    }
