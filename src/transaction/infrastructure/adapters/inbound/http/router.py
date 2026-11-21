
from fastapi import APIRouter, Depends
from http import HTTPStatus
from typing import Annotated

from fastapi.responses import JSONResponse
from src.transaction.application.dto.transaction_response import TransactionResponse
from src.core.dependencies import get_transaction_use_cases

from src.invoice.infrastructure.adapters.transaction_lookup_adapter import TransactionLookupAdapter
from src.transaction.application.TransactionUseCases import TransactionUseCases
from src.transaction.application.dto.transaction_request import TransactionRequest
from src.transaction.application.errorHandler.customer_not_found_exception import CustomerNotFoundException

router = APIRouter()

TransactionUseCasesDependency = Annotated[TransactionUseCases, Depends(get_transaction_use_cases)]
@router.post('/transactions',status_code=HTTPStatus.CREATED, tags=["transaction"])
async def create_transaction(transaction: TransactionRequest,transaction_use_cases: TransactionUseCasesDependency):
    try:
        transaction_validated = TransactionRequest.model_validate(transaction.model_dump())
        return transaction_use_cases.create_transaction(transaction_validated)
    except CustomerNotFoundException as e:
        return JSONResponse(
            status_code=HTTPStatus.NOT_FOUND,
            content={"error": str(e)},
        )
    

@router.get('/transactions', response_model=list[TransactionResponse], tags=["transaction"])
async def get_transactions(transaction_use_cases: TransactionUseCasesDependency):
    return transaction_use_cases.get_transactions()