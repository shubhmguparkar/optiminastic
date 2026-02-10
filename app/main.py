from fastapi import FastAPI
from app.routers import admin, orders, wallet

app = FastAPI(title="Wallet Transaction System")

app.include_router(admin.router)
app.include_router(orders.router)
app.include_router(wallet.router)