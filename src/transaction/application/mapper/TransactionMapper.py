from uuid import uuid4

from ...application.dto.transaction_request import TransactionRequest
from ...application.dto.transaction_response import TransactionResponse
from ...domain.model.Transaction import Transaction

def request_to_domain(request: TransactionRequest) -> Transaction:
    id = uuid4()
    return Transaction(
        id=str(id),
        amount=request.amount,
        description=request.description
    )

def domain_to_response(domain: Transaction) -> TransactionResponse:
    return TransactionResponse(
        id=domain.id,
        amount=str(domain.amount),
        description=domain.description
    )