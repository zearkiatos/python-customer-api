from fastapi import APIRouter

from src.transaction.application.TransactionUseCases import TransactionUseCases
from src.transaction.application.dto.transaction_request import TransactionRequest

router = APIRouter()

@router.post('/transactions', tags=["transaction"])
async def create_transaction(transaction: TransactionRequest):
    transaction_use_cases = TransactionUseCases(None)
    return transaction_use_cases.create_transaction(transaction)