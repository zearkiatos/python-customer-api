from fastapi import APIRouter

from src.customer.infrastructure.adapters.inbound.http.router import router as customer_router
from src.invoice.infrastructure.adapters.inbound.http.router import router as invoice_router
from src.transaction.infrastructure.adapters.inbound.http.router import router as transaction_router
from src.plan.infrastructure.adapters.inbound.http.router import router as plan_router

api_router = APIRouter()
api_router.include_router(customer_router)
api_router.include_router(transaction_router)
api_router.include_router(invoice_router)
api_router.include_router(plan_router)