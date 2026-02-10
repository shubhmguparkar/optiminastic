# create_tables.py
import asyncio
from app.core.database import engine, Base
from app.models.wallet import Wallet
from app.models.ledger import WalletLedger
from app.models.order import Order  # if you have it

async def init():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

asyncio.run(init())
